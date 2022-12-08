from typing import Tuple

import pandas as pd
import os
from scipy.signal import lfilter


def load_data(csv_path_li: list):
    di = {}
    for csv_path in csv_path_li:
        file_name = os.path.basename(csv_path)
        src_df = pd.read_csv(csv_path, sep=",")
        src_df = src_df.loc[src_df['Setpoint'] != 0]
        slices = src_df['Setpoint'].drop_duplicates().to_list()
        for slic in slices:
            di[f"{file_name} [{slic}]"] = {
                'Setpoint': slic,
                'data': src_df['Output'].loc[src_df['Setpoint'] == slic].reset_index(drop=True),
                'control_signal': src_df['PWM'].loc[src_df['Setpoint'] == slic].reset_index(drop=True)
            }
    return di


def convolute(series: pd.Series, conv_size: int = 2):
    if conv_size < 1:
        raise ValueError
    li = []
    for idx in range(len(series)-conv_size+1):
        conv_values = [series[idx + delta] for delta in list(range(conv_size))]
        li.append(sum(conv_values)/conv_size)

    return pd.Series(li, name=series.name)


def linfilter(series: pd.Series, smothness: int) -> pd.Series:
    # the larger smothness is, the smoother curve will be
    b = [1.0 / smothness] * smothness
    a = 1
    return pd.Series(lfilter(b, a, series), name=series.name)


def get_vreg(series: pd.Series, delta: float = 0.05, linfilter_sothness: int = 5, use_lin_filter: bool = False,
             return_smoth_series: bool = False, force_vreg: float = None) -> Tuple[int, float] or Tuple[int, float, pd.Series]:
    if use_lin_filter:
        series = linfilter(series, linfilter_sothness)
    for idx, value in series.iloc[::1].items():
        local_s = series[idx:]
        if force_vreg is None:
            mean = local_s.mean()
        else:
            mean = force_vreg
        # mean_deviance = (local_s/mean)-1
        if all((local_s < (1+delta)*mean) & (local_s > (1-delta)*mean)):
            if use_lin_filter and return_smoth_series:
                return idx, mean, series
            return idx, mean
    return 0, 0


def run():
    di = load_data([os.path.join('data', file) for file in os.listdir('data')])
    # for slic, info in di.items():
    #     print(slic)
    #     print(info.get('data'))
    #     print(convolute(info.get('data')))
    # # linfilter(di.get("plota_logo.csv [40]").get('data'))
    # print(get_vreg(di.get("plota_logo.csv [40]").get('data')))
    print(di)


if __name__ == "__main__":
    run()
