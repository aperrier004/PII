###
# Example of the first UI with an SMI file
###

# WORKING

import os
import numpy as np
import pandas as pd
from PyTrack.formatBridge import generateCompatibleFormat
from PyTrack.Stimulus import Stimulus
from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)

# By default
cwd = os.getcwd()
cwd = cwd.replace("\\", " /")
cwd = cwd.replace(" ", "")
folder_path = cwd + "/PyTrack_examples/Smi/smi_eyetracker_freeviewing.txt"
file_name = "smi_eyetracker_freeviewing"

# Generate a CSV file with a JSON file (from GazePlay)
generateCompatibleFormat(exp_path=folder_path,
                         device="smi",
                         stim_list_mode='NA',
                         start='12',
                         stop='99'
                         )

# Device : smi
# folder_path = cwd + "/PyTrack_examples/Smi/smi_eyetracker_freeviewing.txt"

# Device : tobii
# folder_path = cwd + "/PyTrack_examples/Tobii/tobii_sceneviewing_eyetrack_ascii.txt"


# Get the data from the CSV file by reading it
csvPath = os.path.splitext(folder_path)[0] + ".csv"
# smi
df = pd.read_csv(csvPath)


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
# SMI : path = cwd + "/PyTrack_examples/Smi"
smiPath = cwd + "/Smi"
stim = Stimulus(path=smiPath,
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

        # Use gazePlot() to create a figure that we give to the canva
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

        # Use gazeHeatMap() to create a figure that we give to the canva
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
        # Use visualize() to create a figure that we give to the canva
        #canvas = FigureCanvasTkAgg(stim.visualize(), self)

        # canvas.show()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GazePlayDataVisualizer()
app.mainloop()
