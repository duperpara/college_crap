from typing import List
from math import log, sqrt, e, pi


def rutiruti_jury(li: list) -> list:
    if len(li) <= 1:
        return []
    li_rev = list(reversed(li))
    jury = li[-1] / li_rev[-1]
    jury_li = [jury]
    # if -1 <= jury <= 1:
    new_li = [v1 - v2 * jury for v1, v2 in zip(li, li_rev)][:-1]
    nxt_jury = rutiruti_jury(new_li)
    if nxt_jury:
        jury_li += nxt_jury
    return jury_li


def eval_rutiruti_jury(li):
    jury_result = rutiruti_jury(li)
    print(f'{jury_result=}')
    if max(jury_result) < 1 and min(jury_result) > -1:
        print(f'Stable!')
    else:
        print('Unstable')


def get_ta_so_ereg(tf: List[List[float]]):
    if len(tf[0]) != 2 or len(tf[1]) != 3:
        raise NotImplementedError('only implemented for normal shit')
    print(tf)
    # get_csi_and_wn
    normalized_poli = [item/tf[1][1] for item in tf[1]]

    wn = sqrt(normalized_poli[-1])
    csi = normalized_poli[-2] / (2 * wn)

    return {
        'ta': 4.8 / (csi * wn),
        'So': e ** (-pi * csi / sqrt(1 - csi ** 2)),
        'ereg': tf[0][-1] / tf[1][-1] - 1
    }
