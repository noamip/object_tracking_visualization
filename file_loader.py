import pandas as pd
import csv


def load_file(file):
    if file[-4:] == ".csv":  # a csv file
        fixed_file = fix_csv(file)  # remove illegal rows
        col_names = ["frame", "x", "y", "obj", "size", "seq", "tbd1", "tbd2", "tbd3", "filename", "time", "path_time",
                     "delta_time", "tbd4"]
        use_cols = ["frame", "x", "y", "obj", "size", "seq", "filename", "time",
                    "delta_time"]  # use only relevant columns
        df = pd.read_csv(fixed_file, names=col_names, usecols=use_cols, parse_dates=['time'])  # read file to dataframe
        df['time'] = df['time'] + pd.to_timedelta(df['delta_time'])  # add time column
        df = df.drop(['delta_time'], axis=1)  # remove delta time column

        df = optimize_csv(df)  # optimize data

        file_name = file[:-4]
        file_path = f'{file_name}.pkl.xz'
        file = df.to_pickle(file_path)  # pickle the csv file
    else:  # a pkl file entered
        file_path = file

    return load_pickle(file_path)  # load the pickle file


def fix_csv(csv_file):  # removes wrong format rows from the data file
    lines = []
    file_name = csv_file[:-4]
    with open(csv_file, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if len(row) == 14:
                for i in range(len(row)):
                    row[i] = row[i].strip()
                lines.append(row)
            else:
                continue

    fixed_file_path = f'{file_name}_fixed.csv'
    with open(fixed_file_path, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    readFile.close()
    writeFile.close()

    return fixed_file_path


def optimize_csv(df):  # optimizes the data file to take less space
    df_int = df.select_dtypes(include=['int64'])
    converted_int = df_int.apply(pd.to_numeric, downcast='unsigned')
    df[converted_int.columns] = converted_int
    df_obj = df.select_dtypes(include=['object']).copy()
    converted_obj = pd.DataFrame()

    for col in df_obj.columns:
        num_unique_values = len(df_obj[col].unique())
        num_total_values = len(df_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = df_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = df_obj[col]
    df[converted_obj.columns] = converted_obj
    return df


def load_pickle(pickle):  # loads the pkl file
    return pd.read_pickle(pickle)
