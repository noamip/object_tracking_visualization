import pandas as pd
from pylab import imread
import fix_file as ff
class Model:
    def __init__(self):
        self.NUM_SLICE_Y=10
        self.NUM_SLICE_X=10

    def set_file(self, file, pic):
        self.img = imread(pic)
        self.df = ff.load_file(file)  # 'data/paths.pkl.xz' pd.read_pickle('data/paths.pkl.xz')  #
        self.index_file = self.df.set_index(['filename', 'obj']).sort_index()
        self.df = self.index_file
        self.last = self.index_file  # self.df


    def reset(self):
        self.last = self.df


    def filter_by_hours(self, begin, end):
        objs = self.last.groupby(["filename", "obj"]).agg({'time': ['min', 'max']})
        begin_time = pd.to_datetime(begin).time()
        end_time = pd.to_datetime(end).time()
        min = objs.time['min'].dt.time
        max = objs.time['max'].dt.time
        items = objs[(min.between(begin_time, end_time)) | ((min < begin_time) & (max > begin_time))]
        self.set_last_data(items)
        return self.to_arrays(items)

    def filter_by_date_and_hour(self, date, begin, end):
        objs = self.last.groupby(["filename", "obj"]).agg({'time': ['min', 'max']})
        date = pd.to_datetime(date)
        begin_time = date + pd.to_timedelta(begin)
        end_time = date + pd.to_timedelta(end)
        min = objs[('time', 'min')]
        max = objs[('time', 'max')]
        items = objs[
            (min.between(begin_time, end_time)) | ((min.where(min < begin_time) & (max.where(max > begin_time))))]
        self.set_last_data(items)
        arr = self.to_arrays(items)
        return arr

    def filter_area(self, x0, x1, y0, y1):
        data_a = self.last[(self.last.x.between(x0, x1)) & (self.last.y.between(y0, y1))]
        return data_a

    def filter_by_area(self, x0, x1, y0, y1):
        data_a = self.filter_area(x0, x1, y0, y1)
        self.set_last_data(data_a)
        return self.to_arrays(data_a)

    def filter_by_areas(self, areas):
        width = self.img.shape[1]
        height = self.img.shape[0]
        intersect_series = pd.Series([])
        for squere_index in areas:
            row_index = int(squere_index) // self.NUM_SLICE_Y
            col_index = int(squere_index) - (row_index * self.NUM_SLICE_X)
            top_left = (col_index * (width // self.NUM_SLICE_X), (row_index) * (height // self.NUM_SLICE_Y))
            bottom_right = (
                (col_index + 1) * (width // self.NUM_SLICE_X), (row_index + 1) * (height // self.NUM_SLICE_Y))
            new_series = self.filter_area(top_left[0], bottom_right[0], top_left[1], bottom_right[1])
            if intersect_series.empty:
                intersect_series = new_series
            intersect_series = intersect_series.append(new_series)
        self.set_last_data(intersect_series.groupby(["filename", "obj"]).size())
        return self.to_arrays(intersect_series.groupby(["filename", "obj"]).size())


    def no_filter(self):
        return self.to_arrays(self.last.groupby(["filename", "obj"]).size())

    def to_arrays(self, to_draw):
        points = []
        for t in to_draw.index:
            oo = self.last.loc[t]
            points.append((oo.x, oo.y))
        return points

    def set_last_data(self, data_to_set):
        indexes = set(data_to_set.index.unique())
        last_data = self.index_file[self.index_file.index.isin(indexes)]
        self.last = last_data
