import sympy
from sympy import symbols, acos
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


def table_def(di_str: str = 'di', get_di=False):
    # La = 320
    # Lb = 255
    # Lc = 65
    # Ld = 35
    La, Lb, Lc, Ld = sympy.symbols('La, Lb, Lc, Ld')

    di_di = {
        'reduced_altered_di': {
            "elo": [1, 2, 3],
            "theta": [symbols("θ1"), symbols("θ2") - pi / 2, symbols("θ3")],
            "alpha": [-pi / 2, 0, 0],
            "a": [0, Lb, Lb],
            "d": [Lb, 35, 0],
        },
        'di': {
            "elo": [1, 2, 3, 4, 5, 6],
            "theta": [symbols("θ1"), symbols("θ2") - acos(0), symbols("θ3") + acos(0), symbols("θ4"), symbols("θ5"), symbols("θ6")],
            "alpha": [-acos(0), 0, acos(0), -acos(0), acos(0), 0],
            "a": [0, Lb, 0, 0, 0, 0],
            "d": [La, Ld, 0, Lb, 0, Lc],
        }

    }
    di = di_di.get(di_str)
    if get_di:
        return di

    li = []
    for idx in di.get('elo'):
        li.append(DHStep(**{key: vals[idx-1] for key, vals in di.items()}))

    return li


if __name__ == '__main__':
    import pandas as pd
    print(pd.DataFrame(table_def(get_di=True)))
