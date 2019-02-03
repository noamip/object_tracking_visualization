import cv2
import numpy
from matplotlib import pyplot

np = numpy
plt = pyplot

import pandas as pd
from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs
from pylab import *
from numpy import *
import controller


class View:
    def set_attr(self, pic):  # data/paths.pkl.xz
        self.img = imread(pic)  # "paths0.png"
        self.path_img = pic

    def draw_path(self, to_draw):
        imshow(self.img)
        for x, y in to_draw:
            plot(x, y)
        show()


    def draw_path_one_by_one(self, to_draw):
        imshow(self.img)
        for x, y in to_draw:
            imshow(self.img)
            plot(x, y)
            show()

    def get_filter(self):
        command = input("""enter filter selection:
              1. filter by hours range
              2. filter by date and hours range
              3. filter by specific area
              4. filter by selected areas
              5. no filter 
              6. exit\n""")
        return command

    def get_files(self):
        file = input("enter file\n")
        while file[-7:] != ".pkl.xz" and file[-4:] != ".csv":
            file = input("File is invalid! Enter csv or pkl.xz file!\n")

        picture = input("enter picture\n")

        return file, picture

    def edit(self):
        command = input("""choose edit:
                1. add filter
                2. change filter
                3. no edit\n""")  # 3. view one by one
        return command

    def get_hours(self):
        t1 = input("enter first hour in hh:mm:ss format:\n")
        t2 = input("enter second hour in hh:mm:ss format:\n")
        return (t1, t2)

    def get_date(self):
        date = input("enter date in yyyy-mm-dd format:\n")
        return date

    def get_area(self):
        x0, y0 = input("enter top corner as (x,y):\n").split(',')
        x1, y1 = input("enter bottom corner as (x,y):\n").split(',')
        return (x0, y0, x1, y1)

    def get_areas(self):
        areas = input("enter areas as in pic:\n").split(',')
        return areas

    def draw_grid(self):
        size = 10
        i = 0
        ab = range(size * size)
        im = cv2.imread(self.path_img, 1)
        h, w = im.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        dx, dy = w // size, h // size
        for y in range(size):
            for x in range(size):
                x_place, y_place = int((x * dx + dx / 2) - size), int(y * dy + dy - size)
                cv2.putText(im, str(ab[i]), (x_place, y_place), font, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                i += 1
        for i in range(dy, h, dy):
            im[i:i + 2, :] = 0
        for i in range(dx, w, dx):
            im[:, i:i + 2] = 0
        cv2.imwrite("grid_img.png", im)
        img = imread("grid_img.png")
        imshow(img)
        show()
