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
            'save': self.save,
            'merge': self.merge,
            'merge_select':self.merge_select
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
        self.filters = defaultdict()

    def save(self):  # save current data in current timestmap named file
        tm = time.strftime("%Y%m%d-%H%M%S")
        self.filter_model.get_last_data().to_pickle(f"pickles_can/{tm}.pkz")

    def merge(self):
        data = self.view.last_plotted
        if 0 < len(data) <= int(self.config['path_by_path_limit']):
            self.view.plot_merge_select(self.filter_model.df, data)
            print("after plot")
            self.view.get_routes_for_merge()

        else:
            self.view.status_update("not the right amount of routes for merging.")

    def merge_select(self):
        if len(self.view.get_routes_selected()) != 2:
            self.view.status_update("can only merge 2 routes")
        else:
            oo1,oo2=self.view.get_routes_selected()
            # plt1,plt2= self.filter_model.merge_routes(oo1,oo2)
            indx_list,res=self.filter_model.merge_routes(oo1,oo2)
            self.view.plot_merge_result(indx_list,res)
            # self.view.plot_image_and_routes(res)
           # self.view.plot_points(plt1,plt2)





    def load_data_file(self):  # load data file
        print("in load file")
        self.file = self.view.get_file()  # get the file path from view
        logger.debug(f"got file from view {self.file}")
        if not self.file:
            logger.debug(f"NOOOOO got file from view {self.file}")
            self.view.status_update("No such file in directory. loading default \n")
            self.file = DEFUALT_DATA_FILE
        # self.view.status_update("Loading Data. please wait a while")
        logger.debug(f"got file from view {self.file}")
        self.filter_model.set_file(self.file)  # set the file in model
        print("after set")
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


    def load_image_routes(self):
        self.filters=self.view.get_filters()#get filters selected
        if len(self.filters) == 0:#no filter selected
            self.view.status_update("no filters were selected")
        else:
            print("filters to load",self.filters)
            res= self.filter_model.apply_filters(self.filters)#apply filters on data
            if len(res[1])==0: # no data applies
                self.view.status_update("no data applies")
            else:
                self.view.plot_image_and_routes(res)# draw result on image


    def run(self):
        self.view.master.mainloop()


