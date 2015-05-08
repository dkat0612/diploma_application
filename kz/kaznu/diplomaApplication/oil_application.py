__author__ = 'dk@t'

from tkinter import *
import tkinter as tk
from matplotlib import style
from tkinter import ttk
import kz.kaznu.diplomaApplication.velocity_calc as vc
from matplotlib import pyplot as plt
from pandas import DataFrame as df
import pandas as pd
import tkinter.scrolledtext as tkst
import sys

LARGE_FONT= ("Constantia", 14)
NORM_FONT = ("Constantia", 12)
SMALL_FONT = ("Constantia", 10)
style.use("ggplot")
res = {}

def draw_velocity_graph():
    df.A = pd.read_csv('data/velocity.csv', index_col='r[m]')
    ax = df.A.plot()
    ax.set_ylabel("velocity [m/s]")
    plt.title("Dependence of the radial flow velocity profiles on the water layer thickness sigma")
    plt.show()


class OilApplication(Tk):

    def __init__(self):
        global text
        Tk.__init__(self)
        self.title("Hydrotransport Analysis")
        self.iconbitmap(default="icons/oil.ico")

        self.label = Label(self, text="Hydrotransport analysis application", font=LARGE_FONT, background="#cde2bd")
        self.label.grid(row=0, column=0, sticky=E+W+S+N)
        self.frame = Frame(self)
        self.frame.grid(row=1, column=0, sticky=N+S+E+W)
        self.databox = tkst.ScrolledText(self.frame, background="#eaeaec", width=120)
        self.databox.grid(row=0, column=0, sticky="w")
        self.databox.bind("<1>", lambda event, obj=self.databox: OilApplication.load_data(event, obj))

        self.menu_bar = Menu(self.frame)
        self.file_menu = Menu(self.menu_bar, tearoff=0, background="#849b87")
        self.file_menu.add_command(label="velocity", font=NORM_FONT, command=lambda: self.velocity())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="liquid flow rate", font=NORM_FONT, command=lambda: self.liquid_flow_rate())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", font=NORM_FONT, command=quit)
        self.menu_bar.add_cascade(label="Main", font=SMALL_FONT, menu=self.file_menu)
        Tk.config(self, menu=self.menu_bar)


        # self.button_load = ttk.Button(self, text="Load data")
        # self.button_load.bind("<Button-1>", OilApplication.load_data)
        # self.button_load.grid(row=0, column=10)


    @staticmethod
    def load_data(event, obj):
        file = open("data/velocity.csv", "r", encoding="utf-8")
        text = file.read()
        file.close()
        obj.insert(END, text)


    @staticmethod
    def data_entry_for_popup(popup, text1, text2, row):
        label_1 = ttk.Label(popup, text=text1, font=NORM_FONT, background="#cde2bd")
        label_1.grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(popup)
        entry.grid(row=row, column=1, sticky="w")
        label_2 = ttk.Label(popup, text=text2, font=NORM_FONT, background="#cde2bd")
        label_2.grid(row=row, column=2, sticky="w")
        return entry

    @staticmethod
    def get_data_from_popup():
        global res
        res["r"] = float(res["r"].get())
        res["mu_oil"] = float(res["mu_oil"].get())
        res["p"] = float(res["p"].get())
        res["l"] = float(res["l"].get())
        print(res["r"]," ",res["mu_oil"]," ",res["p"]," ", res["l"], sep="\n")


    @staticmethod
    def velocity():
        popup = tk.Tk()
        popup.wm_title("Velocity")
        Tk.config(popup, bg="#cde2bd")
        res["r"] = OilApplication.data_entry_for_popup(popup, "Radius [R]: ", "m", 1)
        res["mu_oil"] = OilApplication.data_entry_for_popup(popup, "Oil viscosity [mu]: ", "Pa * s", 2)
        res["p"] = OilApplication.data_entry_for_popup(popup, "pressure difference [delta P]: ", "Pa", 3)
        res["l"] = OilApplication.data_entry_for_popup(popup, "distance [L]: ", "km", 4)

        button_ok = ttk.Button(popup, text="OK", command=OilApplication.get_data_from_popup)
        button_ok.grid(row=5, column=0)
        button_draw = ttk.Button(popup, text="DRAW", command=draw_velocity_graph)
        button_draw.grid(row=5, column=2)
        button_draw = ttk.Button(popup, text="CALCULATE", command=OilApplication.calculate_velocity)
        button_draw.grid(row=6, column=0)
        button_close = ttk.Button(popup, text="CLOSE", command=popup.destroy)
        button_close.grid(row=6, column=2)
        popup.mainloop()

    @staticmethod
    def calculate_velocity():
        global text
        r = res["r"]
        mu_oil = res["mu_oil"]
        p = res["p"]
        l = res["l"]
        velocity = vc.Velocity(r, mu_oil, p, l)
        velocity.calculate_and_write()


app = OilApplication()
app.mainloop()






