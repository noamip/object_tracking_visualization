import csv
import datetime
import pickle
import time

from gui_view import Gui_View
from model import Model
import re
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

from settings import DEFUALT_IMAGE_FILE, DEFUALT_DATA_FILE,logger,GENERAL_SETTINGS


class Controller:
    def __init__(self):
        self.config = GENERAL_SETTINGS
        self.m = Model()
        funcs = dict({
            'load_file':self.load_data_file,
            'load_image':self.load_image_file,
            'load_routes':self.load_image_routes,
            'show_grid':self.show_grid,
            'refresh':self.refresh_data,
            'save':self.save
        })
        self.v = Gui_View(funcs)
        self.filters = defaultdict()
        self.has_data = False

    def show_grid(self):
        self.v.show_grid()

    def refresh_data(self):
        self.m.reset()

    def save(self):
        tm = time.strftime("%Y%m%d-%H%M%S")
        self.m.get_last_data().to_pickle(f"data/{tm}.pkl.xz")


    def load_data_file(self):
        print("in load file")
        self.file = self.v.get_file()
        logger.debug(f"got file from view {self.file}")
        # self.file = self.file if self.file  else DEFUALT_DATA_FILE
        if not self.file:
           logger.debug(f"NOOOOO got file from view {self.file}")
           self.v.status_update("No such file in directory. loading default \n")
           self.file = DEFUALT_DATA_FILE
        self.v.status_update("Loading Data. please wait a while")
        logger.debug(f"got file from view {self.file}")
        self.m.set_file(self.file)
        self.has_data = True
        self.v.status_update("Finished Loading Data")

    def load_image_file(self):
        self.image = self.v.get_image()
        logger.debug(f"NOOOOO got image from view {self.image}")
        if not self.image:
           logger.debug(f"NOOOOO got image from view {self.image}")
           self.v.status_update("No such image in directory.\n defualt image loaded")
           self.image = DEFUALT_IMAGE_FILE

        # self.image = self.image if self.image else DEFUALT_IMAGE_FILE
        logger.debug(f"got image from view {self.image}")
        self.v.set_image(self.image)
        self.v.draw_image(self.image)
        self.v.status_update("Finished Loading img")

    def load_image_routes(self):
        if not self.has_data:
            self.v.status_update("Can't load routes with no data you can to load default data with press button")
            return
        # self.filters = self.v.get_filters()
        logger.debug(f"got filters {self.filters}")
        df=None
        if self.v.active_filters['area'].get():
            print("in area")
            area = self.v.area_filter.get()
            x1,y1,x2,y2 = area.split(',')
            df=self.m.filter_by_area(int(x1),int(y1),int(x2),int(y2))
            print("after area")
        if self.v.active_filters['hour'].get():
            print("in hour")
            t1=self.v.first_hour_filter.get()
            t2=self.v.second_hour_filter.get()
            # print(str(t1),str(t2),t1,t2)
            df=self.m.filter_by_hours(str(t1),str(t2))
        if self.v.active_filters['date'].get():
            print("in date")
            t1 = self.v.first_dhour_filter.get()
            t2 = self.v.second_dhour_filter.get()
            date=self.v.date_filter.get()
            df = self.m.filter_by_date_and_hour(date,t1,t2)
        if self.v.active_filters["block"].get():
            areas=self.v.block_filter.get().split(',')
            df=self.m.filter_by_areas(areas)
        self.v.plot_image_and_routes(df)




    def initial_run(self):
        self.v.set_image(self.image)
        self.m.set_file(self.file)
        # self.v.plot_image_and_routes(self.m.get_data(self.filters))


    def run(self):
        self.v.master.mainloop()

    def run2(self):
        self.initial_run()
        self.v.output("Displaying the first 100 rounds.\navailable: filter,grid,config,exit")
        cmd = "init"
        while cmd != 'exit':
            # self.shift_cmd()
            if self.string_found("filter",cmd):
                self.filters = self.v.get_filters(self.filters)
                self.v.plot_image_and_routes(self.m.get_data(self.filters))
            if self.string_found("grid", cmd):
                self.v.draw_grid()
            if self.string_found("config", cmd):
                n_conf = self.v.set_config(self.config)
                self.set_filters(n_conf)
            self.v.output("Enter Command:")
            cmd = self.v.get_input()




    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False

    def set_filters(self,n_conf):
        self.config = n_conf
        self.m.config = self.config
        self.v.config = self.config
        self.v.NUM_SLICE = self.config['num_of_blocks_in_image']
        self.m.NUM_SLICE_X = self.config['num_of_blocks_in_image']
        self.m.NUM_SLICE_Y = self.config['num_of_blocks_in_image']


