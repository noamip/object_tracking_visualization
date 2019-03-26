import pandas as pd
from pylab import imread
import file_loader as ff
from settings import DEFUALT_IMAGE_FILE


class FilterModel:
    def __init__(self):
        self.NUM_SLICE_Y = 10
        self.NUM_SLICE_X = 10

    def set_file(self, file):  # , pic):
        # self.img = imread(pic)
        file_fixer = ff.FileFixer()
        self.df = file_fixer.load_data(file)  # 'data/paths.pkl.xz' pd.read_pickle('data/paths.pkl.xz')  #
        # try:
        #     # self.index_file = self.df.set_index(['filename', 'obj']).sort_index()
        #     self.last = self.df.set_index(['filename', 'obj']).sort_index()
        # except KeyError:
        self.last = self.df
        self.times = self.last.groupby(["filename", "obj"]).agg({'sample_time': ['min', 'max']})


    def reset_data(self):
        self.last = self.df

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
