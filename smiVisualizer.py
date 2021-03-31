###
# Fichier principal permettant d'ouvrir une interface pour afficher des graphiques
###

import numpy as np
import pandas as pd
from PyTrack.formatBridge import generateCompatibleFormat
from Parsing import generateCSV
from PyTrack.Stimulus import Stimulus
from tkinter import ttk
import tkinter as tk
# from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)

# Pour générer le fichier CSV des données
generateCompatibleFormat(exp_path="F:/PII/Smi/smi_eyetracker_freeviewing.txt",
                         device="smi",
                         stim_list_mode='NA',
                         start='12',
                         stop='99'
                         )

# Device : smi
# exp_path = "F:/PII/Smi/smi_eyetracker_freeviewing.txt"

# Device : tobii
# exp_path = "F:/PII/Tobii/tobii_sceneviewing_eyetrack_ascii.txt"


# Fonction qui permet de générer un CSV avec un fichier JSON de gazeplay
# generateCSV("F:/PII/GazePlay/2021-01-12-22-43-15-replayData.json")

# On read le CSV pour avoir les données
# df pour smi
df = pd.read_csv("F:/PII/Smi/smi_eyetracker_freeviewing.csv")

# df pour JSON
#df = pd.read_csv("F:/PII/GazePlay/2021-01-12-22-43-15-replayData.csv")

# A MODIFIER ??? en fonction de si c'est 16:9 ou 4:3
# Dictionary containing details of recording. Please change the values according to your experiment. If no AOI is desired, set aoi value to [0, 0, Display_width, Display_height]
sensor_dict = {
    "EyeTracker":
    {
        "Sampling_Freq": 1000,
        "Display_width": 1280,
        "Display_height": 1024,
        "aoi": [390, 497, 759, 732]
    }
}

# Creating Stimulus object
# SMI : path = "F:/PII/Smi"
# JSON : path = "F:/PII/GazePlay"
stim = Stimulus(path="F:/PII/Smi",
                data=df,
                sensor_names=sensor_dict)

# Some functionality usage
# stim.findEyeMetaData()

# Visualization of plots
# stim.gazePlot(save_fig=True)
# stim.gazeHeatMap(save_fig=True)
# stim.visualize()

####


class GazePlayDataVisualizer(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "GazePlayDataVisualizer")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()

        button4 = ttk.Button(self, text="Heat Map Page",
                             command=lambda: controller.show_frame(PageFour))
        button4.pack()

        button5 = ttk.Button(self, text="Visualizer Page",
                             command=lambda: controller.show_frame(PageFive))
        button5.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Gaze Plot Page !", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # On appelle la fonction gazePlot() pour créer une figure que l'on donne au canvas
        canvas = FigureCanvasTkAgg(stim.gazePlot(), self)

        # canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Heat map Page !", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # On appelle la fonction gazeHeatMap() pour créer une figure que l'on donne au canvas
        canvas = FigureCanvasTkAgg(stim.gazeHeatMap(), self)

        # canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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
        #canvas = FigureCanvasTkAgg(stim.visualize(), self)

        # canvas.show()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GazePlayDataVisualizer()
app.mainloop()