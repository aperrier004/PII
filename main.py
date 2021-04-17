###
# Fichier principal permettant d'ouvrir une interface pour afficher des graphiques
###
from statistiques import active_time
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


def showData():
    global filepath

    if filepath != "":
        csvPath = os.path.splitext(filepath)[0] + ".csv"
        if not os.path.isfile(csvPath):
            # Fonction qui permet de générer un CSV avec un fichier JSON de gazeplay
            generateCSV(filepath)

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

        # Debut de la seconde fenetre
        app2 = tk.Tk()

        # Pour mettre l'application à la taille de l'ecran
        width = app2.winfo_screenwidth()
        height = app2.winfo_screenheight()
        app2.geometry("%dx%d" % (width, height))

        # Icone de la fenetre
        tk.Tk.iconbitmap(app2, default="assets/gazeplayClassicLogo.ico")
        # Titre de la fenetre
        tk.Tk.wm_title(app2, "GazePlayDataVisualizer")

        # ------------------------------- Statistiques  -------------------------------
        # Temps de jeu actif
        con_sec, con_min, con_hour = active_time(
            "F:/PII/GazePlay/bibouleJump.json")

        print("{0}min et {1}s".format(int(con_min), int(con_sec)))

        activeTime = "Temps de jeu actif : " + \
            str(int(con_min)) + "min et " + str(int(con_sec)) + "s"

        label = tk.Label(
            app2, text=activeTime)

        label.pack(pady=10, padx=10)

        # Tirs
        # Taux de réussite xx% (X/Y)
        # Temps de réaction moyen : en s
        # Temps de réaction médian : en s
        # Ecart-type : en s

        # ------------------------------- HEATMAP -------------------------------

        # On appelle la fonction heatmap() pour créer une figure que l'on donne au canvas
        canvasHeatmap = FigureCanvasTkAgg(stim.gazeHeatMap(), app2)
        canvasHeatmap.get_tk_widget().pack(side=tk.TOP, expand=True, anchor=tk.NE)

        toolbarHeatmap = NavigationToolbar2Tk(canvasHeatmap, app2)
        toolbarHeatmap.update()
        # canvasHeatmap._tkcanvas.pack(side=tk.TOP)

        # ------------------------------- GazePlot --------------------------------

        # On appelle la fonction heatmap() pour créer une figure que l'on donne au canvas
        canvasGazePlot = FigureCanvasTkAgg(stim.gazePlot(), app2)
        canvasGazePlot.get_tk_widget().pack(
            side=tk.BOTTOM, expand=True, anchor=tk.SE)

        toolbarGazePlot = NavigationToolbar2Tk(canvasGazePlot, app2)
        toolbarGazePlot.update()

        # canvasGazePlot._tkcanvas.pack(side=tk.LEFT)

        # NE FONCTIONNE PAS
        # ------------------------------- VISUALIZE PLOT -------------------------------

        # On appelle la fonction visualize() pour créer une figure que l'on donne au canvas
        # canvasVisualize = FigureCanvasTkAgg(stim.visualize(), app2)
        # canvasVisualize.get_tk_widget().pack( side=tk.BOTTOM, expand=True, anchor=tk.SE)

        # toolbarVisualize = NavigationToolbar2Tk(canvasVisualize, app2)
        # toolbarVisualize.update()

        app2.mainloop()
    else:
        print("No selected file")


def openfn():
    global filepath
    filepath = filedialog.askopenfilename(
        initialdir="/PII/GazePlay", title="Select A File", filetype=(("json files", "*.json"), ("all files", "*.*")))


# Fenêtre de départ
app = tk.Tk()

# Set an icon to the window
tk.Tk.iconbitmap(app, default="assets/gazeplayClassicLogo.ico")
# Set a title to the window
tk.Tk.wm_title(app, "GazePlayDataVisualizer")

# Pour mettre l'application à la taille de l'ecran
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.geometry("%dx%d" % (width, height))

filepath = "F:/PII/GazePlay/bibouleJump.json"

# Opening image file
img = Image.open('assets/gazeplayClassicLogo.png')
img = img.resize((1000, 300))

photo = ImageTk.PhotoImage(img)
label = tk.Label(app, image=photo)
label.image = photo
label.pack()


browseBtn = tk.Button(
    app, text="Select a .JSON file to start", command=openfn)
browseBtn.pack(pady=20, padx=20)

btnSubmit = tk.Button(app,
                      text="Show graphs",
                      command=showData)
btnSubmit.pack(pady=10, padx=10)


app.mainloop()
