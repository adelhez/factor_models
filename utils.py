import pandas as pd


def align_data_from_time1(data1: pd.DataFrame, data2: pd.DataFrame):
    """Align the dataframe on the starting date. Keep the most recent
    starting date and cut the head accordingly.
    """
    date1 = data1.index[0]
    date2 = data2.index[0]
    if date1 >= date2:
        print(f"Case1: {date1} {date2}")
        return data1, data2.loc[date1:, :]
    elif date1 < date2:
        print(f"Case2: {date2}")
        return data1.loc[date2:, :], data2
    else:
        return data1, data2
    

def align_data_from_time(data_list: list[pd.DataFrame]):
    """Align the dataframe on the starting date. Keep the most recent
    starting date and cut the head accordingly.
    """
    dates = [d.index[0] for d in data_list]
    most_recent_date = max(dates)
    return [d.loc[most_recent_date:, :] for d in data_list]
