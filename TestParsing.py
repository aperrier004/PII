###
# Fichier de tests pour les fonctions de parsing
###
from readingJSON import read_json
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

d = read_json("F:/PII/GazePlay/2021-01-12-22-43-15-replayData.json")

generateCSV("F:/PII/GazePlay/2021-01-12-22-43-15-replayData.json")
