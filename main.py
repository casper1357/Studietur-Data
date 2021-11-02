'''Data fra studietur vist med matplotlib i tkinter
Det er ret recommended kun at tage data fra 1 måned ellers overlapper x-aksens lables, og den er labeled som mm/dd'''

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

studieturdatoer = ["08-30", "08-31", "09-01", "09-02", "09-03"]
casperfiler = ["casperdaily.csv", "casperhourly.csv"]
jacobfiler = "jacobdaily.csv"
gakkifiler = "gakkidaily.csv"
casperdaily = get_data_from_person(casperfiler[0], 5, 10)
casperhourly = get_data_from_person(casperfiler[1], 5, 19)
jacobdaily = get_data_from_person(jacobfiler, 5, 10)
gakkidaily = get_data_from_person(gakkifiler, 5, 10)
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

    def exit_window(self):
        self.window.destroy()

    def create_background(self, filename):
        C = Canvas(self.window, bg="blue", height=0, width=0)
        image = ImageTk.PhotoImage(Image.open(filename))
        imagelabel = Label(self.window, image=image)
        imagelabel.image = image
        imagelabel.place(x=0, y=0, relwidth=1, relheight=1)
        C.pack()

class Plot:
    def __init__(self, window, subplot, figsizex, figsizey, dpi):
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

    def config(self, xlabel="", ylabel="", title="", gridcolor=""):
        self.a1.set_xlabel(xlabel)
        self.a1.set_ylabel(ylabel)
        self.a1.title.set_text(title)
        self.a1.grid(which=BOTH, color=gridcolor)

    def draw(self, xvalues, yvalues, label=""):
        self.a1.plot(xvalues, yvalues, label=label)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=X)
        self.a1.legend()
        self.canvas.draw()

#Laver mit vindue og plotter data fra de forskellige personer på studieturen
def dailyWindow():
    names = ["Casper", "Jacob", "Gakki"]

    data = [casperdaily, jacobdaily, gakkidaily]
    dailywindow = Window(False, root, "Studietur daily", "1920x1080", "white")
    p1 = Plot(dailywindow.window, 111, 10, 4, 50)
    p1.config(xlabel="Dato", ylabel="Skridt", gridcolor="grey")
    draw_persondata(data, names, p1, 1)

    p2 = Plot(dailywindow.window, 111, 10, 4, 50)
    p2.config(xlabel="Dato", ylabel="Duration", gridcolor="grey")
    draw_persondata(data, names, p2, 2)

    p3 = Plot(dailywindow.window, 111, 10, 4, 50)
    p3.config(xlabel="Dato", ylabel="Kalorier", gridcolor="grey")
    draw_persondata(data, names, p3, 3)

    p4 = Plot(dailywindow.window, 111, 10, 4, 50)
    p4.config(xlabel="Dato", ylabel="Etager", gridcolor="grey")
    draw_persondata(data, names, p4, 4)
    dailywindow.loop()

def hourlyWindow():
    names = ["Casper"]
    data = [casperhourly]

    hourlywindow = Window(False, root, "Studietur hourly", "1920x1080", "white")
    p1 = Plot(hourlywindow.window, 111, 10, 4, 50)
    p1.config(xlabel="Dato", ylabel="Skridt", gridcolor="grey")
    draw_persondata(data, names, p1, 1)

    p2 = Plot(hourlywindow.window, 111, 10, 4, 50)
    p2.config(xlabel="Dato", ylabel="Duration", gridcolor="grey")
    draw_persondata(data, names, p2, 2)

    p3 = Plot(hourlywindow.window, 111, 10, 4, 50)
    p3.config(xlabel="Dato", ylabel="Kalorier", gridcolor="grey")
    draw_persondata(data, names, p3, 3)

    p4 = Plot(hourlywindow.window, 111, 10, 4, 50)
    p4.config(xlabel="Dato", ylabel="Etager", gridcolor="grey")
    draw_persondata(data, names, p4, 4)

    hourlywindow.loop()

def menu():
    menuwindow = Window(True, root, "Menu", "1920x1080", "white")
    menuwindow.button("DailySteps", command=dailyWindow)
    menuwindow.button("Hourly", command=hourlyWindow)
    menuwindow.loop()

def draw_persondata(data, names, plot, nr):
    for i in range(len(names)):
        print(data[i])
        plot.draw(data[i][0], data[i][nr], names[i])

menu()