import pandas as pd
import numpy as np

def align_data_from_time(data_list: list[pd.DataFrame]):
    """Align the dataframe on the starting date. Keep the most recent
    starting date and cut the head accordingly.
    """
    dates = [d.index[0] for d in data_list]
    most_recent_date = max(dates)
    return [d.loc[most_recent_date:, :] for d in data_list]


def get_excess_returns(returns: np.ndarray, rf_rates: np.ndarray):
    """Apply the risk-free rates on the returns. The risk-free rates and returns should have the same periodicity, i.e.
    one element in the list correspond to the same period of the other.
    Args:
        returns: np.ndarray: the returns of the asset.
        rf_rates: np.ndarray: the risk-free rates.
    Returns:
        np.ndarray: the excess returns.
    """
    if len(returns) != len(rf_rates):
        print(f"Excess returns {len(returns)} and risk-free rates {len(rf_rates)} should have the same periodicity.")
    return np.array([returns[i] - rf_rates[i] for i in range(0, len(returns))])

def plot_sml():
    pass