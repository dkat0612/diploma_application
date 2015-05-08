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
res = {}

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

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


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
    def data_entry_for_popup(popup, text1, text2, row):
        label_1 = ttk.Label(popup, text=text1, font=NORM_FONT)
        label_1.grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(popup)
        entry.grid(row=row, column=1, sticky="w")
        label_2 = ttk.Label(popup, text=text2, font=NORM_FONT)
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
        res["r"] = OilApplication.data_entry_for_popup(popup, "Radius [R]: ", "m", 1)
        res["mu_oil"] = OilApplication.data_entry_for_popup(popup, "Oil viscosity [mu]: ", "Pa * s", 2)
        res["p"] = OilApplication.data_entry_for_popup(popup, "pressure difference [delta P]: ", "Pa", 3)
        res["l"] = OilApplication.data_entry_for_popup(popup, "distance [L]: ", "km", 4)

        button_ok = ttk.Button(popup, text="OK", command=OilApplication.get_data_from_popup)
        button_ok.grid(row=5, column=0)
        button_clear = ttk.Button(popup, text="CLEAN", command=res.clear)
        button_clear.grid(row=5, column=2)
        button_draw = ttk.Button(popup, text="CALCULATE", command=OilApplication.calculate_velocity)
        button_draw.grid(row=6, column=0)
        button_close = ttk.Button(popup, text="CLOSE", command=popup.destroy)
        button_close.grid(row=6, column=2)
        popup.mainloop()

    @staticmethod
    def calculate_velocity():
        r = res["r"]
        mu_oil = res["mu_oil"]
        p = res["p"]
        l = res["l"]
        velocity = vc.Velocity(r, mu_oil, p, l)
        velocity.calculate_and_write()

app = OilApplication()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()






