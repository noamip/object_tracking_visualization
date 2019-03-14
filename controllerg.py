import time

from gui_view import Gui_View
from filtermodel import FilterModel
from collections import defaultdict
from settings import DEFUALT_IMAGE_FILE, DEFUALT_DATA_FILE, logger, GENERAL_SETTINGS
from coverage.files import os


class Controller:
    def __init__(self):
        self.config = GENERAL_SETTINGS
        self.filter_model = FilterModel()  # hold model instance
        funcs = dict({  # onclick button functions
            'load_file': self.load_data_file,
            'load_image': self.load_image_file,
            'load_routes': self.load_image_routes,
            'show_grid': self.show_grid,
            'refresh': self.refresh_data,
            'save': self.save
        })
        self.view = Gui_View(funcs)  # hold view instance
        self.filters = defaultdict()
        self.has_data = False

    def show_grid(self):  # display grid on image
        self.view.show_grid()

    def refresh_data(self):  # set data state to original file
        if os.path.exists("last.png"):  # if a last state image exists- remove it
            os.remove("last.png")
        self.filter_model.reset_data()

    def save(self):  # save current data in current timestmap named file
        tm = time.strftime("%Y%m%d-%H%M%S")
        self.filter_model.get_last_data().to_pickle(f"data/{tm}.pkl.xz")

    def load_data_file(self):  # load data file
        print("in load file")
        self.file = self.view.get_file()  # get the file path from view
        logger.debug(f"got file from view {self.file}")
        if not self.file:
            logger.debug(f"NOOOOO got file from view {self.file}")
            self.view.status_update("No such file in directory. loading default \n")
            self.file = DEFUALT_DATA_FILE
        self.view.status_update("Loading Data. please wait a while")
        logger.debug(f"got file from view {self.file}")
        self.filter_model.set_file(self.file)  # set the file in model
        self.has_data = True
        self.view.status_update("Finished Loading Data")

    def load_image_file(self):  # load image file
        self.image = self.view.get_image()  # get the image path from view
        logger.debug(f"NOOOOO got image from view {self.image}")
        if not self.image:
            logger.debug(f"NOOOOO got image from view {self.image}")
            self.view.status_update("No such image in directory.\n defualt image loaded")
            self.image = DEFUALT_IMAGE_FILE

        # self.image = self.image if self.image else DEFUALT_IMAGE_FILE
        logger.debug(f"got image from view {self.image}")
        self.view.set_image(self.image)  # set image in view
        self.view.draw_image(self.image)  # display image on screen
        self.view.status_update("Finished Loading img")

    def load_image_routes(self):  # display the routes
        if not self.has_data:
            self.view.status_update("Can't load routes with no data you can to load default data with press button")
            return
        logger.debug(f"got filters {self.filters}")
        df = None
        if self.view.active_filters['area'].get():  # if filter by area is selected
            print("in area")
            area = self.view.area_filter.get()
            x1, y1, x2, y2 = area.split(',')
            df = self.filter_model.filter_by_area(int(x1), int(x2), int(y1), int(y2))
            print("after area")
        if self.view.active_filters['hour'].get():  # if filter by time is selected
            print("in hour")
            t1 = self.view.first_hour_filter.get()
            t2 = self.view.second_hour_filter.get()
            df = self.filter_model.filter_by_hours(str(t1), str(t2))
            print("after hour",len(df))
        if self.view.active_filters['date'].get():  # if filter by date+time is selected
            print("in date")
            t1 = self.view.first_dhour_filter.get()
            t2 = self.view.second_dhour_filter.get()
            date = self.view.date_filter.get()
            df = self.filter_model.filter_by_date_and_hour(date, t1, t2)
        if self.view.active_filters["block"].get():  # if filter by areas is selected
            areas = self.view.block_filter.get().split(',')
            df = self.filter_model.filter_by_areas(areas)
        if len(df) ==0:
            self.view.draw_image(self.image)
            self.view.status_update("no data applies")
        self.view.plot_image_and_routes(df)

    def run(self):
        self.view.master.mainloop()

