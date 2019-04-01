import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import pandas as pd
from coverage.files import os
import matplotlib.ticker as plticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings import logger
from settings import GENERAL_SETTINGS


# from tkinter import *


class Gui_View:
    def __init__(self, functs_setup):
        self.funcs = functs_setup
        master = tk.Tk()
        self.master = master
        self.set_window_init()

        # self.len_param = {'area': 4, 'hour': 2, 'date': 3}

        self.config = GENERAL_SETTINGS
        if os.path.exists("last.png"):
            os.remove("last.png")

    event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

    def set_window_init(self):
        self.master.title("Parse Routes")
        self.draw_top_panel()
        # self.place_holder()
        self.draw_filters()
        # self.draw_bottom_panel()

    def draw_top_panel(self):  # draw image and file entries
        self.master_panel = tk.Frame(self.master, borderwidth=2, bg='white')
        self.master_panel.grid(padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        self.file_button = tk.Button(self.master_panel, text="Load File", command=self.funcs['load_file'],
                                     width=10, height=1, bg='lightGray', font=("Arial", 11))
        self.file_button.config(font=("Arial", 11))
        self.file_button.grid()
        self.file_entry = tk.Entry(self.master_panel, width=20)
        # self.file_entry.config(font=("Arial", 11))
        self.file_entry.grid(row=0, column=1, padx=(5, 0))

        self.image_button = tk.Button(self.master_panel, text="Load Image", command=self.funcs['load_image'],
                                      width=10, height=1, bg='lightGray', font=("Arial", 11))
        self.image_button.grid(row=0, column=2, padx=(10, 0))
        # self.image_button.config(font=("Arial", 11))
        self.img_entry = tk.Entry(self.master_panel, width=20)
        self.img_entry.config(font=("Arial", 11))
        self.img_entry.grid(row=0, column=3, padx=(5, 0))

    def draw_filters(self):  # draw filters panel
        self.active_filters = {"area": tk.IntVar(), "hour": tk.IntVar(), "date": tk.IntVar(), "block": tk.IntVar()}
        self.label_filters = tk.Label(self.master_panel, text="Filters:", bg='white', font=("Arial", 14)).grid(
            row=1, column=4, columnspan=2, sticky=tk.W)

        # area filter ======================================
        self.area_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Area",
                                            variable=self.active_filters['area'], bg='white', font=("Arial", 11))
        self.area_checkbox.grid(row=2, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Enter top and bottom corners as x1,y1,x2,y2:", bg='white',
                 font=("Arial", 9)).grid(
            sticky=tk.W, row=3, column=4)
        self.area_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.area_filter.grid(row=3, column=5)

        # hour filter ======================================
        self.hour_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Time",
                                            variable=self.active_filters['hour'], bg='white', font=("Arial", 11))

        self.hour_checkbox.grid(row=4, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Enter first hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=5, column=4)
        self.first_hour_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.first_hour_filter.grid(row=5, column=5)
        tk.Label(self.master_panel, text="Enter second hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=6, column=4)
        self.second_hour_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.second_hour_filter.grid(row=6, column=5)

        # date filter ======================================
        self.date_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Date",
                                            variable=self.active_filters['date'], bg='white', font=("Arial", 11))
        self.date_checkbox.grid(row=7, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Enter date as yyyy-mm-dd:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=8, column=4)

        self.date_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.date_filter.grid(row=8, column=5)
        tk.Label(self.master_panel, text="Enter first hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=9, column=4)
        self.first_dhour_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.first_dhour_filter.grid(row=9, column=5)
        tk.Label(self.master_panel, text="Enter second hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=10, column=4)
        self.second_dhour_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.second_dhour_filter.grid(row=10, column=5)

        # multiple areas==========

        self.block_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Block",
                                             variable=self.active_filters['block'], bg='white', font=("Arial", 11))
        self.block_checkbox.grid(row=11, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Enter desired areas as in grid:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=12, column=4)
        self.block_filter = tk.Entry(self.master_panel, width=25, bg='white')
        self.block_filter.grid(row=12, column=5)

        # load routes button=============
        self.filters_button = tk.Button(self.master_panel, text="Load Routes", command=self.funcs['load_routes'],
                                        height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.filters_button.grid(row=13, column=4, columnspan=1, pady=(6, 0))
        # show grid button=============
        self.grid_button = tk.Button(self.master_panel, text="Show Grid", command=self.funcs['show_grid'],
                                     height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.grid_button.grid(row=13, column=5, columnspan=1, pady=(6, 0))

        # refresh button=============
        self.refresh = tk.Button(self.master_panel, text="Refresh Data", command=self.funcs['refresh'],
                                 height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.refresh.grid(row=14, column=4, columnspan=1, pady=(6, 0))

        # merge button=============
        self.merge = tk.Button(self.master_panel, text="Merge Routes", command=self.funcs['merge'],
                               height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.merge.grid(row=14, column=5, columnspan=1, pady=(6, 0))

        # save button=============
        self.save = tk.Button(self.master_panel, text="Save Current", command=self.funcs['save'],
                              height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.save.grid(row=15, column=4, columnspan=1, pady=(6, 0))

    def draw_image(self, image_name):  # display image on screen
        image = plt.imread(image_name)
        self.fig = plt.figure()  # figsize=(5, 4)
        im = plt.imshow(image)  # later use a.set_data(new_data)

        plt.subplots_adjust(top=0.9, bottom=0.3, right=0.9, left=0.1, hspace=0, wspace=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master_panel)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, rowspan=13, sticky=tk.W + tk.E + tk.N + tk.S,
                                         padx=(10, 10))

        # cid=self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    # def onclick(self,event):
    #         print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #               ('double' if event.dblclick else 'single', event.button,
    #                event.x, event.y, event.xdata, event.ydata))

    def plot_image_and_routes(self, data_obj):
        dataframe, df_obj = data_obj
        # df_obj = df_obj.head(15)
        l = len(df_obj)
        self.last_plotted = df_obj
        self.data = dataframe
        logger.debug(f"plotting {l} routes")

        lim = int(self.config['path_by_path_limit'])
        max_lim = int(self.config['start_draw_heatmap_limit'])
        logger.debug(f"l={l},lim={lim},max_lim={max_lim}")
        if l < max_lim and l > lim:
            self.plot_all_routes(dataframe, df_obj)
        elif l <= lim:
            MsgBox = tk.messagebox.askquestion('One by One?', 'Would you like to plot routes one by one?')
            if MsgBox == 'yes':
                self.plot_one_by_one(dataframe, df_obj)
            else:
                self.plot_all_routes(dataframe, df_obj)
        else:
            self.plot_heatmap(dataframe, df_obj)

    def plot_all_routes(self, dataframe, df_obj):
        logger.debug(f"entering plot_all_routes with {len(df_obj)} routes")
        im = plt.imread(self.image_name)
        plt.imshow(im)
        # self.draw_grid()
        for t in df_obj.index:
            oo = dataframe.loc[t]
            plt.plot(oo.x, oo.y)
        plt.savefig('last.png', transparent=True, bbox_inches='tight', pad_inches=-0.3)
        self.canvas.draw()
        plt.gcf().clear()

    def plot_heatmap(self, dataframe, df_obj):
        logger.debug(f"entering plot_heatmap with {len(df_obj)} routes")
        im = plt.imread(self.image_name)
        plt.imshow(im)
        count = pd.DataFrame({'count': dataframe.loc[df_obj.index].groupby(["x", "y"]).size()}).reset_index()
        mat_count = count.pivot('y', 'x', 'count').values
        plt.imshow(mat_count, cmap=plt.get_cmap("hsv"), interpolation='nearest')
        plt.colorbar()
        # plt.pause(0.5)
        # plt.gcf().clear()
        self.canvas.draw()
        plt.gcf().clear()

    def plot_one_by_one(self, dataframe, df_obj):
        logger.debug(f"entering plot_one_by_one with {len(df_obj)} routes")
        im = plt.imread(self.image_name)
        # self.draw_grid()
        for t in df_obj.index:
            plt.imshow(im)
            oo = dataframe.loc[t]
            plt.plot(oo.x, oo.y)
            self.canvas.draw()
            self.master.after(500)
            plt.gcf().clear()

    def show_grid(self):  # draws grid on image
        logger.debug(f"enter draw grid ")
        if os.path.exists("last.png"):  # if there were filters applied
            im = plt.imread("last.png", 0)
        else:
            im = plt.imread(self.image_name)

        im_size = im.shape[:2]
        width = im_size[1]
        height = im_size[0]

        ax = self.fig.add_subplot(111)

        myInterval_w = width // int(self.config['num_of_blocks_in_image'])
        myInterval_h = height // int(self.config['num_of_blocks_in_image'])

        loc_w = plticker.MultipleLocator(base=myInterval_w)
        loc_h = plticker.MultipleLocator(base=myInterval_h)

        ax.xaxis.set_major_locator(loc_w)
        ax.yaxis.set_major_locator(loc_h)

        # Add the grid
        ax.grid(which='major', axis='both', linestyle='-', color="k")

        # Add the image
        ax.imshow(im)

        # Find number of gridsquares in x and y direction
        nx = abs(int(float(ax.get_xlim()[1] - ax.get_xlim()[0]) / float(myInterval_w)))
        ny = abs(int(float(ax.get_ylim()[1] - ax.get_ylim()[0]) / float(myInterval_h)))

        # Add some labels to the gridsquares
        for j in range(ny):
            y = myInterval_h / 2 + j * myInterval_h
            for i in range(nx):
                x = myInterval_w / 2. + float(i) * myInterval_w
                ax.text(x, y, '{:d}'.format(i + j * nx), color='k', ha='center', va='center')

        self.canvas.draw()
        plt.gcf().clear()

    def get_file(self):  # returns the data file path entered
        if not os.path.exists(self.file_entry.get()):
            return None
        return self.file_entry.get()

    def get_image(self):  # returns the image file path entered
        if not os.path.exists(self.img_entry.get()):
            return None
        return self.img_entry.get()

    def error_input(self, msg):
        self.status_message.configure(text=f"Curropted input. Task aborted:{msg}")

    def status_update(self, msg):
        messagebox.showinfo("Parse Routes", f"{msg}")
        # self.status_message.configure(text=f"{msg}")

    def set_image(self, image_name):  # sets image
        self.image_name = image_name
        self.img = plt.imread(image_name)

    def plot_merge(self, dataframe, df_obj):
        logger.debug(f"entering plot_all_routes with {len(df_obj)} routes")
        im = plt.imread(self.image_name)
        plt.imshow(im)
        i = 0
        for t in df_obj.index:
            oo = dataframe.loc[t]
            plt.plot(oo.x, oo.y, label=f"{i}")
            i += 1
        plt.legend()
        self.canvas.draw()
        plt.gcf().clear()

    def get_filters(self):
        filters = {}
        if self.active_filters['hour'].get():
            t1 = self.first_hour_filter.get()
            t2 = self.second_hour_filter.get()
            filters['hour'] = (t1, t2)

        if self.active_filters['area'].get():
            area = self.area_filter.get()
            x1, y1, x2, y2 = area.split(',')
            filters['area'] = (int(x1), int(x2), int(y1), int(y2))

        if self.active_filters['date'].get():
            t1 = self.first_dhour_filter.get()
            t2 = self.second_dhour_filter.get()
            date = self.date_filter.get()
            filters['date'] = (date, t1, t2)

        if self.active_filters['block'].get():
            areas = self.block_filter.get().split(',')
            filters['block'] = areas

        return filters

    def get_routes_for_merge(self):
        print('in get routes')
        self.routes_root = tk.Tk()

        yScroll = tk.Scrollbar(self.routes_root, orient=tk.VERTICAL)
        yScroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.routes = tk.Listbox(self.routes_root, selectmode='multiple', yscrollcommand=yScroll.set)

        for i in range(len(self.last_plotted)):
            self.routes.insert(i, i)
        self.routes.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        yScroll['command'] = self.routes.yview
        tk.Button(self.routes_root, text='merge', command=self.show_entry_fields).grid(column=1, sticky=tk.E, pady=4)
        self.routes_root.mainloop()
        print('after get routes')

    def show_entry_fields(self):
        if len(self.routes.curselection()) != 2:
            self.status_update("can only merge 2 routes")
        else:
            r1, r2 = self.routes.curselection()
            print(r1, r2)
            plt.imshow(self.img)
            oo1 = self.data.loc[self.last_plotted.index[r1]]

            last_x = oo1.x[-1]
            last_y = oo1.y[-1]

            oo2 = self.data.loc[self.last_plotted.index[r2]]
            first_x = oo2.x[0]
            first_y = oo2.y[0]

            points_x,points_y = get_line(last_x,last_y,first_x,first_y)
            to_plot_x = pd.concat([oo1.x,points_x, oo2.x])
            to_plot_y = pd.concat([oo1.y,points_y,oo2.y])
            plt.plot(to_plot_x, to_plot_y)
            self.canvas.draw()
        self.routes_root.destroy()


def get_line(x1, y1, x2, y2):
    points_x = pd.Series()
    points_y = pd.Series()
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points_x.add(y)
            points_y.add(x)
        else:
            points_x.add(x)
            points_y.add(y)
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points_x.reindex(index=points_x.index[::-1])
        points_y.reindex(index=points_y.index[::-1])
    return (points_x,points_y)