import pandas as pd
import os
from scipy.signal import lfilter


def load_data(csv_path_li: list):
    di = {}
    for csv_path in csv_path_li:
        file_name = os.path.basename(csv_path)
        src_df = pd.read_csv(csv_path, sep=";")
        src_df = src_df.loc[src_df['Setpoint'] != 0]
        slices = src_df['Setpoint'].drop_duplicates().to_list()
        for slic in slices:
            di[f"{file_name} [{slic}]"] = {
                'Setpoint': slic,
                'data': src_df['Output'].loc[src_df['Setpoint'] == slic].reset_index(drop=True)
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


def linfilter(series: pd.Series, smothness: int):
    # the larger smothness is, the smoother curve will be
    b = [1.0 / smothness] * smothness
    a = 1
    return lfilter(b, a, series)


def get_vreg(series: pd.Series, delta: float = 0.05):
    print(series.mean())
    for idx, value in series.iloc[::1].items():
        local_s = series[idx:]
        mean = local_s.mean()
        # print((local_s-mean > delta*mean))
        # print((local_s-mean < -delta*mean))
        if all((local_s-mean < delta*mean) & (local_s-mean > -delta*mean)):
            print(f'vreg ({idx+1} onward): {series[idx+1:].mean()}')
            return

def run():
    di = load_data([os.path.join('data', file) for file in os.listdir('data')])
    for slic, info in di.items():
        print(slic)
        print(info.get('data'))
        print(convolute(info.get('data')))
    linfilter(di.get("plota_logo.csv [40]").get('data'))
    get_vreg(di.get("plota_logo.csv [40]").get('data'))

if __name__ == "__main__":
    run()
