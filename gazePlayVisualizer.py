###
# Fichier principal permettant d'ouvrir une interface pour afficher des graphiques
###

# NE FONCTIONNE PAS
import os
import pandas as pd
from PyTrack.formatBridge import generateCompatibleFormat
from Parsing import generateCSV
from PyTrack.Stimulus import Stimulus
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
# from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")

# CONSTANTS
LARGE_FONT = ("Verdana", 12)


class GazePlayDataVisualizer(tk.Tk):
    """
    A class used to represent the application
    """

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data = {
            "filepath": tk.StringVar(),
            # NOT SURE ABOUT THAT
            "stim": Stimulus,
        }

        tk.Tk.iconbitmap(self, default="assets/gazeplayClassicLogo.ico")
        tk.Tk.wm_title(self, "GazePlayDataVisualizer")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.filepath = ""

        for F in (StartPage, MenuPage, PageOne, PageTwo, PageThree, PageFour, PageFive):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(
            self, text="GazePlay Data Visualizer", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        def generateData(filepath):
            if filepath != "":

                # Fonction qui permet de générer un CSV avec un fichier JSON de gazeplay
                generateCSV(filepath)

                # On read le CSV pour avoir les données
                csvPath = os.path.splitext(filepath)[0] + ".csv"
                df = pd.read_csv(csvPath)

                # TODO ??? en fonction de si c'est 16:9 ou 4:3
                # Dictionary containing details of recording. Please change the values according to your experiment. If no AOI is desired, set aoi value to [0, 0, Display_width, Display_height]
                sensor_dict = {
                    "EyeTracker":
                    {
                        "Sampling_Freq": 1000,
                        "Display_width": 1980,
                        "Display_height": 1080,
                        "aoi": [0, 0, 1980, 1080]
                    }
                }

                # Creating Stimulus object
                # os.getcwd() gets the current working directory
                stim = Stimulus(path=os.getcwd(),
                                data=df,
                                sensor_names=sensor_dict)
                self.controller.shared_data["stim"] = stim
                print("test stim")
                print(stim)

        def openfn():
            filepath = filedialog.askopenfilename(
                initialdir="/PII/GazePlay", title="Select A File", filetype=(("json files", "*.json"), ("all files", "*.*")))
            self.controller.shared_data["filepath"].set(filepath)
            generateData(filepath)
            controller.show_frame(MenuPage)
            return filepath

        browseBtn = ttk.Button(
            self, text="Select a .JSON file to start", command=openfn)
        browseBtn.pack()

        # Opening image file
        img = Image.open('assets/gazeplayClassicLogo.png')
        img = img.resize((1000, 300))

        photo = ImageTk.PhotoImage(img)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.pack()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Menu", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnRestart = ttk.Button(self, text="Start with another file",
                                command=lambda: controller.show_frame(StartPage))
        btnRestart.pack()

        btnPage1 = ttk.Button(self, text="Heatmap",
                              command=lambda: controller.show_frame(PageOne))
        btnPage1.pack()

        btnPage2 = ttk.Button(self, text="Gazeplot",
                              command=lambda: controller.show_frame(PageTwo))
        btnPage2.pack()

        # USELESS POTENTIELLEMENT (tout ce qu'il y a en dessous)
        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        filepath = self.controller.shared_data["filepath"].get()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Heatmap", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnBack = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MenuPage))
        btnBack.pack()

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        stim = self.controller.shared_data["stim"]
        print("stim de page One")
        print(stim)

        print("page One avant canvas")

        # On appelle la fonction gazeHeatMap() pour créer une figure que l'on donne au canvas
        canvas = FigureCanvasTkAgg(stim.gazeHeatMap(), self)

        # canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        print("page One après canvas")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="GazePlot", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        btnBack = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MenuPage))
        btnBack.pack()

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, event):
        stim = self.controller.shared_data["stim"].get()

        # On appelle la fonction gazePlot() pour créer une figure que l'on donne au canvas
        canvas = FigureCanvasTkAgg(stim.gazePlot(), self)

        # canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Gaze Plot Page !", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Heat map Page !", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Visualizer Page !", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # ERROR
        # On appelle la fonction visualize() pour créer une figure que l'on donne au canvas
        # canvas = FigureCanvasTkAgg(stim.visualize(), self)

        # canvas.show()
        # canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GazePlayDataVisualizer()
app.mainloop()
