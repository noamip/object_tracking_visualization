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
        min = objs.time['min'].dt.time  # objs[('time','min')]
        max = objs.time['max'].dt.time  # objs[('time','max')]
        items = objs[(min.between(begin_time, end_time)) | ((min < begin_time) & (max > begin_time))]
        self.set_last_data(items)
        return self.to_arrays(items)

    def no_filter(self):
        return self.to_arrays(self.last.groupby(["filename", "obj"]).size())

    def to_arrays(self, to_draw):
        points = []
        for t in to_draw.index:
            oo = self.last.loc[t]
            # imshow(self.img)
            points.append((oo.x, oo.y))
        return points

    def set_last_data(self, data_to_set):
        indexs = set(data_to_set.index.unique())
        last_data = self.index_file[self.index_file.index.isin(indexs)]
        self.last = last_data
