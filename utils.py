import pandas as pd


# Allow to compare dataset and make them start
# from the same date.
def align_data_from_time(data1: pd.DataFrame, data2: pd.DataFrame):
    date1 = data1.index[0]
    date2 = data2.index[0]
    if date1 >= date2:
        return data1, data2.loc[date1:, :]
    elif date1 < date2:
        return data1.loc[date2:, :], data2
    else:
        return data1, data2