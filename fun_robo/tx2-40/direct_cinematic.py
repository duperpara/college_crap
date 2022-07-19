from sympy import symbols
from math import pi


class DHStep:
    def __init__(self, elo, theta, alpha, a, d):
        self.elo = elo
        self.theta = theta
        self.alpha = alpha
        self.a = a
        self.d = d

    def __str__(self):
        return f"{self.elo} | {self.theta} | {self.alpha} | {self.a} | {self.d}"

    def __repr__(self):
        return self.__str__()


def table_def(get_di=False):
    di = {
        "elo": [1, 2, 3],
        "theta": [symbols("θ1"), symbols("θ2")-pi/2, symbols("θ3")],
        "alpha": [-pi/2, 0, pi/2],
        "a": [0, 225, 225],
        "d": [225, 35, 0],
    }
    if get_di:
        return di

    li = []
    for idx in di.get('elo'):
        li.append(DHStep(**{key: vals[idx-1] for key, vals in di.items()}))

    return li


if __name__ == '__main__':
    import pandas as pd
    print(pd.DataFrame(table_def(get_di=True)))
