__author__ = 'dk@t'

import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from matplotlib import style
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
import kz.kaznu.diplomaApplication.velocity_calc as vc

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)
style.use("ggplot")

f = Figure()
a = f.add_subplot(111)


def draw_velocity_graph(i):
    pull_data = open("data/velocity.txt", "r").read()
    data_list = pull_data.split('\n')
    x_list = []
    y_list = []
    for eachLine in data_list:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            x_list.append(int(x))
            y_list.append(int(y))

    a.clear()
    a.plot(x_list, y_list)

def animate(i):
    pullData = open("data/test.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


class OilApplication(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="icons/oil.ico")
        tk.Tk.wm_title(self, "Hydrotransport Analysis")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(container)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="velocity", font=LARGE_FONT, command=lambda: self.velocity())
        file_menu.add_separator()
        file_menu.add_command(label="liquid flow rate", font=LARGE_FONT, command=lambda: self.liquid_flow_rate())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", font=LARGE_FONT, command=quit)
        menu_bar.add_cascade(label="Main", font=LARGE_FONT, menu=file_menu)

        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    @staticmethod
    def data_for_popup(popup, text1, text2, row):
        label_1 = ttk.Label(popup, text=text1, font=NORM_FONT)
        label_1.grid(row=row, column=0, sticky="w")
        entry_r = ttk.Entry(popup)
        entry_r.grid(row=row, column=1, sticky="w")
        label_2 = ttk.Label(popup, text=text2, font=NORM_FONT)
        label_2.grid(row=row, column=2, sticky="w")
        return entry_r.get()

    @staticmethod
    def velocity():
        popup = tk.Tk()
        popup.wm_title("Velocity")

        r = OilApplication.data_for_popup(popup, "Radius [R]: ", "m", 1)
        mu_oil = OilApplication.data_for_popup(popup, "Oil viscosity [mu]: ", "Pa * s", 2)
        p = OilApplication.data_for_popup(popup, "pressure difference [delta P]: ", "Pa", 3)
        l = OilApplication.data_for_popup(popup, "distance [L]: ", "km", 4)

        button_draw = ttk.Button(popup, text="Calculate", command=OilApplication.calculate_velocity(r, mu_oil, p, l))
        button_draw.grid(row=5, column=0)
        button_ok = ttk.Button(popup, text="OK", command=popup.destroy)
        button_ok.grid(row=5, column=1)
        popup.mainloop()

    @staticmethod
    def calculate_velocity(r, mu_oil, p, l):
        velocity = vc.Velocity(r, mu_oil, p, l)
        velocity.calculate_and_write()

app = OilApplication()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()


"""
        label_r = ttk.Label(popup, text="Radious: ", font=NORM_FONT)
        label_r.grid(row=1, column=0, sticky="w")
        entry_r = ttk.Entry(popup)
        entry_r.grid(row=1, column=1, sticky="w")
        r = entry_r.get()

        label_mu = ttk.Label(popup, text="Oil viscosity: ", font=NORM_FONT)
        label_mu.grid(row=2, column=0, sticky="w")
        entry_mu = ttk.Entry(popup)
        entry_mu.grid(row=2, column=1, sticky="w")
        mu_oil = entry_mu.get()

        label_p = ttk.Label(popup, text="pressure difference: ", font=NORM_FONT)
        label_p.grid(row=3, column=0, sticky="w")
        entry_p = ttk.Entry(popup)
        entry_p.grid(row=3, column=1, sticky="w")
        p = entry_p.get()

        label_l = ttk.Label(popup, text="distance [L]: ", font=NORM_FONT)
        label_l.grid(row=4, column=0, sticky="w")
        entry_l = ttk.Entry(popup)
        entry_l.grid(row=4, column=1, sticky="w")
        l = entry_l.get()
"""




