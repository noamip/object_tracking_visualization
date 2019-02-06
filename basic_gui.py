import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        self.set_window_init()

    def set_window_init(self):
        self.master.title("Parse Routes")

        self.master_panel = tk.Frame(self.master, borderwidth=2, bg='white')
        self.master_panel.grid(padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        self.file_button = tk.Button(self.master_panel, text="Load File", command=self.draw_image,
                                     width=10, height=1, bg='white', font=("Arial", 11))
        self.file_button.config(font=("Arial", 11))
        self.file_button.grid()

        self.file_entry = tk.Entry(self.master_panel, width=20)
        self.file_entry.grid(row=0, column=1, padx=(5, 0))

        self.image_button = tk.Button(self.master_panel, text="Load Image", command=self.draw_image,
                                      width=10, height=1, bg='white', font=("Arial", 11))
        self.image_button.grid(row=0, column=2, padx=(10, 0))

        self.img_entry = tk.Entry(self.master_panel, width=20)
        self.img_entry.config(font=("Arial", 11))
        self.img_entry.grid(row=0, column=3, padx=(5, 0))

        self.draw_image()
        self.draw_filters()

        self.status_message = tk.Message(self.master_panel, text="Program Output", bg='white', borderwidth=5,width=200,
                                         highlightbackground="black", highlightthickness=1, font=("Arial", 14)).grid(
            sticky=tk.W + tk.E + tk.N + tk.S, row=19, column=0, columnspan=4,rowspan=2)

    def draw_image(self):
        image = plt.imread('paths0.png')  # TODO call to defualt image
        fig = plt.figure()
        im = plt.imshow(image)
        plt.subplots_adjust(top=0.9, bottom=0.3, right=0.9, left=0.1,
                            hspace=0, wspace=0)

        canvas = FigureCanvasTkAgg(fig, master=self.master_panel)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, columnspan=4, rowspan=20, sticky=tk.W + tk.E + tk.N + tk.S,
                                    padx=(10, 10), pady=(10, 10))

    def draw_filters(self):
        self.active_filters = {"area": tk.IntVar(), "hour": tk.IntVar(), "date": tk.IntVar(), "block": tk.IntVar()}
        self.label_filters = tk.Label(self.master_panel, text="Filters:", bg='white', font=("Arial", 14)).grid(
            row=1, column=4, columnspan=2, sticky=tk.W)

        # area filter ======================================
        self.area_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Area",
                                            variable=self.active_filters['area'], bg='white', font=("Arial", 11)).grid(row=2, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Insert top and buttom corners x0,y0,x1,y1 :", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=3, column=4)
        self.area_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=3, column=5)

        # hour filter ======================================
        self.hour_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Time",
                                            variable=self.active_filters['hour'], bg='white', font=("Arial", 11)).grid(row=4, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Insert first hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=5, column=4)
        self.hour_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=5, column=5)
        tk.Label(self.master_panel, text="Insert second hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=6, column=4)
        self.hour_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=6, column=5)

        # date filter ======================================
        self.date_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Date",
                                            variable=self.active_filters['date'], bg='white', font=("Arial", 11)).grid(row=7, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="Insert date as dd-mm-yyyy :", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=8, column=4)

        self.date_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=8, column=5)

        tk.Label(self.master_panel, text="Insert first hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=9, column=4)
        self.date_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=9, column=5)

        tk.Label(self.master_panel, text="Insert second hour as hh:mm:ss:", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=10, column=4)
        self.date_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=10, column=5)

        #grid filter ===================================
        self.block_checkbox = tk.Checkbutton(self.master_panel, text="Filter by Block",
                                             variable=self.active_filters['block'], bg='white', font=("Arial", 11)).grid(row=11, column=4, sticky=tk.W)
        tk.Label(self.master_panel, text="select areas :", bg='white', font=("Arial", 9)).grid(
            sticky=tk.W, row=12, column=4)
        self.block_filter = tk.Entry(self.master_panel, width=25, bg='white').grid(row=12, column=5)

        #load-filters button
        self.filters_button = tk.Button(self.master_panel, text="Load Filters", command=self.draw_image,
                                       height=1,width=30, bg='white', font=("Arial", 11)).grid(row=13, column=4,columnspan=2)


root = tk.Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
