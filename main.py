###
# Fichier principal permettant d'ouvrir une interface pour afficher des graphiques
###
from statistiques import active_time, gameName, goal, goalToReach
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
        baseName = os.path.basename(filepath)
        fileName = os.path.splitext(baseName)[0]

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
                        name=fileName,
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
        title = "Visualisation des données du fichier " + \
            filepath + " correspondant au jeu " + gameName(filepath)
        lblTitle = tk.Label(
            app2, text=title)
        lblTitle.pack(side=tk.TOP)
        # Temps de jeu actif
        con_sec, con_min, con_hour = active_time(filepath)

        strActiveTime = "Temps de jeu actif : " + \
            str(int(con_min)) + "min et " + \
            str(int(con_sec)) + "s"

        # Tirs
        nbGoal = goal(filepath)
        strGoal = "Tirs : " + str(nbGoal)

        # Taux de réussite xx% (X/Y)
        nbGoalToReach = goalToReach(filepath)
        sucess = nbGoal/nbGoalToReach * 100
        strGoalToReach = "Taux de réussite : " + str(sucess) + "% (" + \
            str(nbGoal) + "/" + str(nbGoalToReach) + ")"

        # Temps de réaction moyen : en s
        # Temps de réaction médian : en s
        # Ecart-type : en s

        strStats = strActiveTime + "\n\n" + strGoal + "\n\n" + strGoalToReach + "\n\n"

        lblTemps = tk.Label(
            app2, text=strStats)
        lblTemps.pack(side=tk.LEFT)

        right_frame = tk.Frame(app2)
        left_frame = tk.Frame(app2)

        # ------------------------------- HEATMAP -------------------------------

        # On appelle la fonction heatmap() pour créer une figure que l'on donne au canvas
        canvasHeatmap = FigureCanvasTkAgg(stim.gazeHeatMap(), right_frame)
        canvasHeatmap.get_tk_widget().grid(row=0, column=1)
        canvasHeatmap.get_tk_widget().update()

        toolbar_frame1 = tk.Frame(right_frame)
        toolbar_heatmap = NavigationToolbar2Tk(canvasHeatmap, toolbar_frame1)
        toolbar_frame1.grid(row=1, column=1)
        toolbar_heatmap.update()
        toolbar_frame1.update()

        # ------------------------------- GazePlot --------------------------------

        # On appelle la fonction heatmap() pour créer une figure que l'on donne au canvas
        canvasGazePlot = FigureCanvasTkAgg(stim.gazePlot(), right_frame)
        canvasGazePlot.get_tk_widget().grid(row=2, column=1)
        canvasGazePlot.get_tk_widget().update()

        toolbar_frame2 = tk.Frame(right_frame)
        toolbar_gaze_plot = NavigationToolbar2Tk(
            canvasGazePlot, toolbar_frame2)
        toolbar_frame2.grid(row=3, column=1)
        toolbar_gaze_plot.update()
        toolbar_frame2.update()

        right_frame.pack(side=tk.RIGHT)
        right_frame.update()

        # ------------------------------- VISUALIZE PLOT -------------------------------

        # On appelle la fonction visualize() pour créer une figure que l'on donne au canvas
        canvasVisualize = FigureCanvasTkAgg(stim.visualize(), left_frame)
        canvasVisualize.get_tk_widget().grid(row=0, column=1)
        canvasVisualize.get_tk_widget().update()

        toolbar_frame3 = tk.Frame(left_frame)
        toolbarVisualize = NavigationToolbar2Tk(
            canvasVisualize, toolbar_frame3)
        toolbar_frame3.grid(row=1, column=1)
        toolbarVisualize.update()
        toolbar_frame3.update()

        left_frame.pack(side=tk.LEFT)
        left_frame.update()

        # END

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


# Par défaut
cwd = os.getcwd()
cwd = cwd.replace("\\", " /")
cwd = cwd.replace(" ", "")
filepath = cwd + "/GazePlay/bibouleJump.json"

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


def quit():
    app.destroy()


app.protocol("WM_DELETE_WINDOW", quit)

app.mainloop()
