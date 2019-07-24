import copy
import pandas as pd
from pylab import imread
import file_loader as ff
from settings import DEFUALT_IMAGE_FILE

# print("in set file", self.last.head(5))
# gg = self.last.head(5)
# gg = gg.reset_index()
# print("in set file reset\n", gg, len(gg))
# ss = pd.DataFrame({"filename": "tttt.txt", "obj": 1111, "frame": 1, "x": 100, "y": 100, "size": 100, "seq": 100,
#                    "start": self.last.head(1).start
#                       , "path_time": self.last.head(1).path_time, "delta_time": self.last.head(1).delta_time,
#                    "sample_time": self.last.head(1).sample_time})
# ss.set_index(["filename", "obj"])
# gg = gg.append(ss)
# # print("in init", len(self.last), len(self.df))
# print("in set file append", gg, len(gg))

from coverage.files import os
class FilterModel:
    def __init__(self):
        self.NUM_SLICE_Y = 10
        self.NUM_SLICE_X = 10

    def set_file(self, file):  # , pic):
        file_fixer = ff.FileFixer()
        self.df = file_fixer.load_data(file)# 'data/paths.pkl.xz' pd.read_pickle('data/paths.pkl.xz')  #
        self.last = self.df
        self.times = self.last.groupby(["filename", "obj"]).agg({'sample_time': ['min', 'max']})

    def reset_data(self):
        self.last = self.df
        print("data_refreshed",len(self.last),len(self.df))

    def filter_by_hours(self, begin, end):  # filter by specific hour range
        # objs = self.last.groupby(["filename", "obj"]).agg({'sample_time': ['min', 'max']})
        # convert strings to datetime
        begin_time = pd.to_datetime(begin).time()
        end_time = pd.to_datetime(end).time()

        min = self.times.sample_time['min'].dt.time  # begining of the path
        max = self.times.sample_time['max'].dt.time  # end of the path

        items = self.times[(min.between(begin_time, end_time)) | (
                (min < begin_time) & (max > begin_time))]  # only paths in the time range

        self.set_last_data(items)
        return items
        # return self.to_arrays(items)

    def filter_by_date_and_hour(self, date, begin, end):  # filter by specific date and hour range
        # objs = self.last.groupby(["filename", "obj"]).agg({'sample_time': ['min', 'max']})
        # convert strings to datetime
        date = pd.to_datetime(date)

        begin_time = date + pd.to_timedelta(begin)
        end_time = date + pd.to_timedelta(end)

        min = self.times[('sample_time', 'min')]  # begining of the path
        max = self.times[('sample_time', 'max')]  # end of the path
        try:
            items = self.times[(min.between(begin_time, end_time)) | (
                (min.where(min < begin_time) & (max.where(max > begin_time))))]  # only paths in the date + time range
        except BaseException:
            items = pd.DataFrame()

        self.set_last_data(items)
        # arr = self.to_arrays(items)
        return items

    def filter_area(self, x0, x1, y0, y1):  # returns data in specified area
        data_a = self.last[(self.last.x.between(x0, x1)) & (self.last.y.between(y0, y1))]
        # data_a = self.last[((x0<= self.last.x) & (self.last.x <= x1)& (y0<=self.last.y) & (self.last.y <= y1))]
        return data_a

    def filter_by_area(self, x0, x1, y0, y1):  # filter by selecting a speific area by  top and bottom points
        # print("in area")
        data_a = self.filter_area(x0, x1, y0, y1)
        self.set_last_data(data_a)
        # print("after")
        # return self.to_arrays(data_a)
        return data_a

    def filter_by_areas(self, areas):  # filter by selecting sprecific areas by predefined image slices
        img = imread(DEFUALT_IMAGE_FILE)
        width = img.shape[1]
        height = img.shape[0]
        intersect_series = pd.Series([])
        for squere_index in areas:  # go over each desired area
            row_index = int(squere_index) // self.NUM_SLICE_Y  # find its row
            col_index = int(squere_index) - (row_index * self.NUM_SLICE_X)  # find its column
            top_left = (col_index * (width // self.NUM_SLICE_X),
                        (row_index) * (height // self.NUM_SLICE_Y))  # tuple of top left indexes
            bottom_right = (
                (col_index + 1) * (width // self.NUM_SLICE_X),
                (row_index + 1) * (height // self.NUM_SLICE_Y))  # tuple of bottom right indexes
            new_series = self.filter_area(top_left[0], bottom_right[0], top_left[1],
                                          bottom_right[1])  # send to filter area with the coordinates
            if intersect_series.empty:  # no data in it yet
                intersect_series = new_series
            intersect_series = intersect_series.append(new_series)  # add to the result

        self.set_last_data(intersect_series.groupby(["filename", "obj"]).size())
        return intersect_series.groupby(["filename", "obj"]).size()

    def set_last_data(self, data_to_set):  # set last data state
        indexes = set(data_to_set.index.unique())
        self.last = self.last[self.last.index.isin(indexes)]

    def get_last_data(self):  # return last data state
        return self.last

    def apply_filters(self, filters):
        intersect_series = self.last.groupby(["filename", "obj"]).size().sort_values(ascending=False)
        # print(" in apply\n ",self.last.head(5))
        if 'hour' in filters.keys():
            new_series = self.filter_by_hours(filters['hour'][0], filters['hour'][1])
            # logger.debug(f"found {len(new_series)} routes by hour")
            indx_list = intersect_series.index.intersection(new_series.index)
            intersect_series = intersect_series.loc[indx_list]

        if 'area' in filters.keys():
            new_series = self.filter_by_area(filters['area'][0], filters['area'][1], filters['area'][2],
                                             filters['area'][3])
            # logger.debug(f"found {len(new_series)} routes by area")
            indx_list = intersect_series.index.intersection(new_series.index)
            intersect_series = intersect_series.loc[indx_list]

        if 'date' in filters.keys():
            new_series = self.filter_by_date_and_hour(filters['date'][0], filters['date'][1], filters['date'][2])
            # logger.debug(f"found {len(new_series)} routes by date")
            indx_list = intersect_series.index.intersection(new_series.index)
            intersect_series = intersect_series.loc[indx_list]

        if 'block' in filters.keys():
            new_series = self.filter_by_areas(filters['block'])
            # logger.debug(new_series.head(3))
            intersect_series = intersect_series[intersect_series.isin(new_series)]
            indx_list = intersect_series.index.intersection(new_series.index)
            intersect_series = intersect_series.loc[indx_list]

        print("got ", len(intersect_series))
        return (self.last, intersect_series)

    def merge_routes(self, oo1, oo2):
        last_x = oo1.x[-1]
        last_y = oo1.y[-1]

        first_x = oo2.x[0]
        first_y = oo2.y[0]

        print("last.type",type(self.last))

        points_x, points_y = get_line(last_x, last_y, first_x, first_y)
        to_plot_x = pd.concat([oo1.x, points_x, oo2.x])
        to_plot_y = pd.concat([oo1.y, points_y, oo2.y])
       #!!!!!!!!!!!! print("oo1.filename",oo1.index.levels[0])

        new_filename=list(oo1.index.levels[0])[-1]
        new_obj=list(oo1.index.levels[1])[-1]
        new_frame = oo1.frame[-1]
        new_stime = oo1.sample_time[-1]
        new_ptime = oo1.path_time[-1]
        new_dtime = oo1.delta_time[-1]
        new_start=oo1.start[-1]
        new_seq = oo1.seq[-1]
        new_size = oo1.size

        print("before",len(self.last),len(oo1.x),"len oo1",len(oo1))

        print("columns",list(self.last.columns.values))

        last = copy.deepcopy(self.last)

        if os.path.exists("temp.csv"):
         os.remove("temp.csv")


        i=0
        # print("before reset last\n", self.last.head(5))
        self.last=self.last.reset_index()
        # print("after reset last\n", self.last.head(5))
        for x, y in zip(to_plot_x, to_plot_y):
            new_row = pd.DataFrame({"filename":new_filename,"obj":new_obj,"frame":new_frame, "x":x,"y":y,"size":new_size,"seq":new_seq,"start":new_start,"path_time":new_ptime,"delta_time":new_dtime,"sample_time":new_stime},index=["filename", "obj"])
            self.last = self.last.append(new_row,ignore_index=True)
            i += 1


        print("after last\n", self.last.head(2),"\n",self.last.tail(3))#, self.last.index.levels
        print("after", len(self.last), len(oo1.x), "len oo1", len(oo1))

        intersect_series = self.last.groupby(["filename", "obj"]).size().sort_values(ascending=False)
        self.last = self.last.set_index(["filename", 'obj']).sort_index()
        # print("indx_list ", len(indx_list))
        print("got ", len(intersect_series))
        # print("last\n",self.last.head(5))
        return(intersect_series,self.last)



def get_line(x1, y1, x2, y2):
    points_x = pd.Series()
    points_y = pd.Series()
    issteep = abs(y2 - y1) > abs(x2 - x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2 - y1)
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
    return (points_x, points_y)
