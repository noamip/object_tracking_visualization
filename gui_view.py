import tkinter as tk
import matplotlib.pyplot as plt
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
        self.draw_bottom_panel()

    def draw_top_panel(self):#draw image and file entries
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

    def draw_filters(self):#draw filters panel
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

        # show grid button=============
        self.refresh = tk.Button(self.master_panel, text="Refresh Data", command=self.funcs['refresh'],
                                 height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.refresh.grid(row=14, column=4, columnspan=1, pady=(6, 0))

        # save button=============
        self.save = tk.Button(self.master_panel, text="Save Current", command=self.funcs['save'],
                              height=1, width=17, bg='lightGray', font=("Arial", 11))
        self.save.grid(row=14, column=5, columnspan=1, pady=(6, 0))

    def draw_bottom_panel(self):#draw output-status panel
        self.status_message = tk.Message(self.master_panel, text="Program Output", bg='lightGray', borderwidth=5,
                                         anchor=tk.NW,
                                         width=800, highlightbackground="black", highlightthickness=1,
                                         font=("Arial", 14))
        self.status_message.grid(row=14, column=0, columnspan=4)



    def draw_image(self, image_name):#display image on screen
        image = plt.imread(image_name)
        self.fig = plt.figure()  # figsize=(5, 4)
        im = plt.imshow(image)  # later use a.set_data(new_data)

        plt.subplots_adjust(top=0.9, bottom=0.3, right=0.9, left=0.1, hspace=0, wspace=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master_panel)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, rowspan=13, sticky=tk.W + tk.E + tk.N + tk.S,
        padx=(10, 10))

        cid=self.fig.canvas.mpl_connect('button_press_event', self.onclick)


    def onclick(self,event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))





    def plot_image_and_routes(self, data_obj):
        l = len(data_obj)
        logger.debug(f"plotting {l} routes")
        lim = int(self.config['path_by_path_limit'])
        # max_lim = int(self.config['start_draw_heatmap_limit'])
        logger.debug(f"l={l},lim={lim}")
        if l > lim:
            self.plot_all_routes(data_obj)
        else:
            self.plot_one_by_one(data_obj)

    def plot_all_routes(self, to_draw):  # plot all routes together
        logger.debug(f"entering plot_all_routes with {len(to_draw)} routes")
        im = plt.imread(self.image_name)
        print(f"in plot all routes len {len(to_draw)}")
        plt.imshow(im)
        for x, y in to_draw:
            plt.plot(x, y)
        plt.savefig('last.png', transparent=True, bbox_inches='tight', pad_inches=-0.3)
        self.canvas.draw()
        plt.gcf().clear()
        print("after plot all routes")

    def plot_one_by_one(self, to_draw):  # plot each route individually
        logger.debug(f"entering plot_one_by_one with {len(to_draw)} routes")
        # im = plt.imread(self.image_name)
        # self.draw_grid()
        for x, y in to_draw:
            im = plt.imread(self.image_name)
            plt.imshow(im)
            plt.plot(x, y)
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

    # def place_holder(self):
    #     print("button clicked")

    def error_input(self, msg):
        self.status_message.configure(text=f"Curropted input. Task aborted:{msg}")

    def status_update(self, msg):
        self.status_message.configure(text=f"{msg}")

    def set_image(self, image_name):  # sets image
        self.image_name = image_name
        self.img = plt.imread(image_name)



