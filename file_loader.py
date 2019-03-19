import pandas as pd
import csv

from settings import logger
import os.path

class FileFixer:
    def fix_corrupted_file(self, file_name, fixed_path, corrupted_path):
        logger.debug(
            f"entering fix_corrupted_file,file_name={file_name},fixed_path={fixed_path},corrupted_path={corrupted_path}")
        # logger.error(file_name)

        valid_counter = 0
        invalid_counter = 0
        # for line in fileinput.input(file_name):
        with open(file_name, 'r') as datar, open(fixed_path, "w") as fixedw, open(
                corrupted_path,
                "w",
                encoding="utf-8") as errorw:

            for line in datar.readlines():
                if (len(line.split(', ')) == 14):
                    fixedw.write(line.strip(" "))
                    valid_counter += 1
                else:
                    errorw.write(line.strip(" "))
                    invalid_counter += 1

        logger.error(f"{valid_counter} valid lines.")
        # print(f"{valid_counter} valid lines.")
        logger.error(f"{invalid_counter} corrupted lines. See {corrupted_path}")


    def optimize_csv_file(self, file_name):
        logger.debug(f"entering optimize_csv_file,file_name={file_name}")

        cols_types = dict({
            'delta_time': 'object',
            'filename': 'category',
            'frame': 'uint16',
            'obj': 'uint16',
            'path_time': 'object',
            'seq': 'uint16',
            'size': 'uint32',
            'x': 'uint16',
            'y': 'uint16'})

        cols = ["frame", "x", "y", "obj", "size", "seq", "tbd1", "tbd2", "tbd3", "filename", "start", "path_time",
                "delta_time", "tbd4"]
        useful_cols = ["frame", "x", "y", "obj", "size", "seq", "filename", "start", "path_time", "delta_time"]

        df = pd.read_csv(file_name, names=cols, usecols=useful_cols, dtype=cols_types, parse_dates=['start'],
                         infer_datetime_format=True)

        logger.debug(f"optimize_csv_file: finished reading csv file")

        df = self.set_time_row(df)
        df = self.set_general_index(df)
        # df = self.remove_duplicates()

        return df


    def load_data(self, file_name):
        # print("Loading Data...\nThis may take a while.")
        logger.debug(f"entering load_data,file_name={file_name}")

        file_name_only = os.path.splitext(os.path.basename(file_name))[0]
        logger.debug(f"file name only - {file_name_only}")
        self.fixed_file = f"data/fixed_{file_name_only}.csv"

        if not os.path.exists(self.fixed_file):
            curr_f = f"data/corrupted_{file_name_only}.csv"
            self.fix_corrupted_file(file_name, self.fixed_file, curr_f)

        if not os.path.exists("pickles_can"):
            logger.debug(f"create directory pickles_can")
            os.makedirs("pickles_can")

        if not os.path.exists(f"pickles_can/{file_name_only}.pkz"):
            df = self.optimize_csv_file(self.fixed_file)
            self.dump_to_pickle(df, file_name_only)

        self.data = pd.read_pickle(f"pickles_can/{file_name_only}.pkz")
        return self.data



    def set_general_index(self, df):
        logger.debug(f"entering set_index")
        df_by_obj = df.set_index(['filename', 'obj']).sort_index()

        return df_by_obj


    def dump_to_pickle(self, df, pickle_name):
        logger.debug(f"entering dump_to_pickle")
        self.data = f"pickles_can/{pickle_name}.pkz"
        df.to_pickle(f"pickles_can/{pickle_name}.pkz")


    def set_time_row(self, df):
        logger.debug(f"entering set_time_row")

        df['sample_time'] = df.start
        df['sample_time'] += pd.to_timedelta(df['delta_time'])

        df.drop('start', 1)
        df.drop('delta_time', 1)
        df.drop('path_time', 1)

        return df
