'''Data fra studietur vist med matplotlib i tkinter
Det er ret recommended kun at tage data fra 1 måned ellers overlapper x-aksens labels, og den er labeled som mm/dd'''

from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd

root = Tk()

def get_values(columnind, filename):
    df = pd.read_csv(filename)
    #Da excel filen kun har et element for både column og row bliver vi nødt til at tage det første element for columns og derefter splitte alle values
    allvalues = df[df.columns[0]].tolist()
    values = []
    for i in range(len(allvalues)):
        value = allvalues[i].split(";")
        #index = 1 er antal steps i excel, 2 duration osv, ændre dette, hvis der skal tages data fra en anden column.
        values.append(value[columnind])
    return values

#Skulle ændre datatypen af en liste for at dagene på x-aksen og y-aksen ikke ser forfærdelige ud
def lst_str_to_int(lst):
    new_lst = []
    if type(lst[0]) == str:
        for i in lst:
            new_lst.append(int(i))
    return new_lst

def get_dage(csvfilename, startind, endind):
    #Det var et kæmpe mess at få splittet datoerne op så ja...
    datoer = get_values(0, csvfilename)
    dage = []
    for i in range(len(datoer)):
        #Måned/dage er fra index 5:10, hvis man bare vil have dag så er det 08:10, husk også at rette det i studieturdatoer
        dage.append(datoer[i][startind:endind])
    return dage

def get_data_from_person(filename, startind, endind):
    persondage = get_dage(filename, startind, endind)
    personskridt = lst_str_to_int(get_values(1, filename))
    personduration = lst_str_to_int(get_values(2, filename))
    personcalories = lst_str_to_int(get_values(4, filename))
    personfloors = lst_str_to_int(get_values(5, filename))
    return [persondage, personskridt, personduration, personcalories, personfloors]

def draw_persondata(data, names, plot, nr):
    for i in range(len(names)):
        plot.draw(data[i][0], data[i][nr], names[i])

studieturdatoer = ["08-30", "08-31", "09-01", "09-02", "09-03"]
casperfiler = ["casperdaily.csv", "casperhourly.csv"]
jacobfiler = "jacobdaily.csv"
gakkifiler = "gakkidaily.csv"
casperdaily = get_data_from_person(casperfiler[0], 5, 10)
casperhourly = get_data_from_person(casperfiler[1], 5, 19)
jacobdaily = get_data_from_person(jacobfiler, 5, 10)
gakkidaily = get_data_from_person(gakkifiler, 5, 10)
dailydata = [casperdaily, jacobdaily, gakkidaily]
hourlydata = [casperhourly]
dailynames = ["Casper", "Jacob", "Mathias"]
hourlynames = ["Casper"]


class Window:
    def __init__(self, mainwindow, root, title, geometry, bgcolor, icon=""):
        self.mainwindow = mainwindow
        if self.mainwindow == False:
            self.window = Toplevel(root)
        else:
            self.window = root

        self.bgcolor = bgcolor
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.configure(bg=bgcolor)
        self.window.iconbitmap(icon)

    def label(self, message, textcolor):
        Label(self.window, text=message, bg=textcolor).pack()

    def loop(self):
        self.window.mainloop()

    def button(self, text, command):
        b = Button(self.window, text=text, command=command)
        b.pack()

    def exit(self):
        self.window.destroy()
        self.window.update()

    def create_background(self, filename):
        C = Canvas(self.window, bg="blue", height=0, width=0)
        image = ImageTk.PhotoImage(Image.open(filename))
        imagelabel = Label(self.window, image=image)
        imagelabel.image = image
        imagelabel.place(x=0, y=0, relwidth=1, relheight=1)
        C.pack()

class Plot:
    def __init__(self, window, subplot, figsizex, figsizey, dpi):
        self.dontDraw = False
        self.plt = plt
        self.window = window
        # Figure with size and dpi (pixels) Example: 6.4 figsize and 100 dpi is 6.4 * 100 = 640 pixels
        self.fig = Figure(figsize=(figsizex, figsizey), dpi=dpi)
        # Adding a subplot
        self.a1 = self.fig.add_subplot(subplot)
        # Creating a canvas on TK
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        # Adding the toolbar from matplotlib to tkinter canvas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)
        # axis labels
        self.a1.set_xlabel('x')
        self.a1.set_ylabel('y')
        self.a1.title.set_text("Plot x")

    def config(self, xlabel="", ylabel="", title="", gridcolor="", rotation=0, labelsize=10):
        #Hvis du bruger rotation er der ikke længere mulighed for at bruge toolbaren
        self.a1.tick_params(axis='x', labelrotation=rotation, labelsize=labelsize)
        self.a1.tick_params(axis='y', labelrotation=rotation, labelsize=labelsize)
        self.a1.set_xlabel(xlabel)
        self.a1.set_ylabel(ylabel)
        self.a1.title.set_text(title)
        self.a1.grid(which=BOTH, color=gridcolor)
        self.a1.yaxis.label.set_size(40)
        self.a1.xaxis.label.set_size(40)

    def draw(self, xvalues, yvalues, label=""):
        self.a1.plot(xvalues, yvalues, label=label)
        self.toolbar.update()
        if not self.dontDraw:
            self.canvas.get_tk_widget().pack()
        self.a1.legend()
        self.canvas.draw()

def menu():
    menuwindow = Window(True, root, "Menu", "1920x1080", "white")
    menuwindow.button("DailySteps", command=dailystepswin)
    menuwindow.button("Hourly", command=hourlystepswin)
    menuwindow.loop()

def dailystepswin():
    dailysteps = Window(False, root, "Daily steps", "1920x1080", "white")
    dailysteps.button(text="Next", command=lambda: [f() for f in [dailysteps.exit, dailydurwin]])
    p1 = Plot(dailysteps.window, 111, 45, 15, 50)
    p1.config(xlabel="Dato", ylabel="Skridt", gridcolor="grey", labelsize=30)
    draw_persondata(dailydata, dailynames, p1, 1)
    dailysteps.loop()

def dailydurwin():
    dailyduration = Window(False, root, "Daily duration", "1920x1080", "white")
    dailyduration.button(text="Next", command=lambda: [f() for f in [dailyduration.exit, dailycalwin]])
    p2 = Plot(dailyduration.window, 111, 45, 15, 50)
    p2.config(xlabel="Dato", ylabel="Duration", gridcolor="grey", labelsize=30)
    draw_persondata(dailydata, dailynames, p2, 2)
    dailyduration.loop()

def dailycalwin():
    dailycalories = Window(False, root, "Daily calories", "1920x1080", "white")
    dailycalories.button(text="Next", command=lambda: [f() for f in [dailycalories.exit, dailyfloorswin]])
    p3 = Plot(dailycalories.window, 111, 45, 15, 50)
    p3.config(xlabel="Dato", ylabel="Kalorier", gridcolor="grey", labelsize=30)
    draw_persondata(dailydata, dailynames, p3, 3)
    dailycalories.loop()

def dailyfloorswin():
    dailyfloors = Window(False, root, "Daily floors", "1920x1080", "white")
    dailyfloors.button(text="Next", command=lambda: [f() for f in [dailyfloors.exit, dailystepswin]])
    p4 = Plot(dailyfloors.window, 111, 45, 15, 50)
    p4.config(xlabel="Dato", ylabel="Etager", gridcolor="grey", labelsize=30)
    draw_persondata(dailydata, dailynames, p4, 4)
    dailyfloors.loop()

def hourlystepswin():
    hourlystepswindow = Window(False, root, "Hourly steps", "1920x1080", "white")
    hourlystepswindow.button(text="Next", command=lambda: [f() for f in [hourlystepswindow.exit, hourlydurwin]])
    p1 = Plot(hourlystepswindow.window, 111, 45, 20, 50)
    p1.config(xlabel="Dato", ylabel="Skridt", gridcolor="grey", rotation=90, labelsize=15)
    draw_persondata(hourlydata, hourlynames, p1, 1)
    hourlystepswindow.loop()

def hourlydurwin():
    hourlydurationwindow = Window(False, root, "Hourly duration", "1920x1080", "white")
    hourlydurationwindow.button(text="Next", command=lambda: [f() for f in [hourlydurationwindow.exit, hourlycalwin]])
    p2 = Plot(hourlydurationwindow.window, 111, 45, 20, 50)
    p2.config(xlabel="Dato", ylabel="Duration", gridcolor="grey", rotation=90, labelsize=15)
    draw_persondata(hourlydata, hourlynames, p2, 2)
    hourlydurationwindow.loop()

def hourlycalwin():
    hourlycalorieswindow = Window(False, root, "Hourly calories", "1920x1080", "white")
    hourlycalorieswindow.button(text="Next", command=lambda: [f() for f in [hourlycalorieswindow.exit, hourlyfloorswin]])
    p3 = Plot(hourlycalorieswindow.window, 111, 45, 20, 50)
    p3.config(xlabel="Dato", ylabel="Kalorier", gridcolor="grey", rotation=90, labelsize=15)
    draw_persondata(hourlydata, hourlynames, p3, 3)
    hourlycalorieswindow.loop()

def hourlyfloorswin():
    hourlyfloorswindow = Window(False, root, "Hourly floors", "1920x1080", "white")
    hourlyfloorswindow.button(text="Next", command=lambda: [f() for f in [hourlyfloorswindow.exit, hourlystepswin]])
    p4 = Plot(hourlyfloorswindow.window, 111, 45, 20, 50)
    p4.config(xlabel="Dato", ylabel="Etager", gridcolor="grey", rotation=90, labelsize=15)
    draw_persondata(hourlydata, hourlynames, p4, 4)
    hourlyfloorswindow.loop()

menu()
