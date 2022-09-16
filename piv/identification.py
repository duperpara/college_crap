import pandas as pd

def run():
    full_series = pd.read_csv('de_10_em_10.csv', sep=';')['Output']
    print(full_series)

    delta_h_data_di = {
        's_20_to_30': {
            'data': full_series[232:283].reset_index(drop=True),
            'delta_pwm': 10,
            'delta_t': 283-232,
        },
        's_30_to_40': {
            'data': full_series[358:419].reset_index(drop=True),
            'delta_pwm': 10,
            'delta_t': 419-358,
        },
        's_40_to_50': {
            'data': full_series[442:537].reset_index(drop=True),
            'delta_pwm': 10,
            'delta_t': 537-442,
        },
        's_50_to_60': {
            'data': full_series[596:762].reset_index(drop=True),
            'delta_pwm': 10,
            'delta_t': 762-596,
        },
    }

    delta_h_data_di = delta_data(delta_h_data_di)
    delta_h_data_di = calculate_delta_h(delta_h_data_di)
    delta_h_data_di = calculate_k(delta_h_data_di)
    delta_h_data_di = calculate_yts(delta_h_data_di)
    delta_h_data_di = calculate_tau(delta_h_data_di)
    delta_h_data_di = calculate_teta(delta_h_data_di)


    print(delta_h_data_di)


def delta_data(di):
    for key, item in di.items():
        di[key]['data'] = item.get('data')-min(item.get('data'))
    return di


def calculate_delta_h(di):
    for key, item in di.items():
        di[key]['delta_h'] = item.get('data')[len(item.get('data'))-1] - item.get('data')[0]
    return di


def calculate_k(di):
    for key, item in di.items():
        di[key]['k'] = item.get('delta_pwm')/item.get('delta_h')
    return di


def calculate_yts(di):
    for key, item in di.items():
        di[key]['yt1_SM'] = (28.3/100)*max(item.get('data'))
        di[key]['t1_SM'] = min(item.get('data')[item.get('data') > di[key]['yt1_SM']])
        di[key]['yt2_SM'] = (63.2/100)*max(item.get('data'))
        di[key]['t2_SM'] = min(item.get('data')[item.get('data') > di[key]['yt2_SM']])

    return di


def calculate_tau(di):
    for key, item in di.items():
        di[key]['tau_SM'] = 1.5*(item.get('t2_SM')-item.get('t1_SM'))
    return di


def calculate_teta(di):
    for key, item in di.items():
        teta_SM = item.get('t2_SM')-item.get('tau_SM')
        di[key]['teta_SM'] = teta_SM if teta_SM > 0 else 0
    return di




if __name__ == '__main__':
    run()
