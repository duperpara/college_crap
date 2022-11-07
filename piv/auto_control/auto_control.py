from collections.abc import Callable
from typing import Tuple, List
import math

import control
import numpy as np


def _default_ta_score_function(ta: float) -> float:
    return abs(100/ta)


def _default_s0_score_function(s0: float) -> float:
    return abs(1/s0)


def _default_ereg_score_function(ereg: float) -> float:
    return abs(1/ereg)


def optimize_pi_controller(
        *,
        tf_function: Callable[[float, float], Tuple[List[float], List[float]]],
        ta_score_function: Callable[[float], float] = _default_ta_score_function,
        s0_score_function: Callable[[float], float] = _default_s0_score_function,
        ereg_score_function: Callable[[float], float] = _default_ereg_score_function,
        optimize_type: str = 'dot_grid',

        resolution: float = 0.1,
        kp_range: Tuple[float, float] = None,
        ki_range: Tuple[float, float] = None,
        auto_range: bool = True,
):
    return _OptimizePIController(
        tf_function=tf_function,
        ta_score_function=ta_score_function,
        s0_score_function=s0_score_function,
        ereg_score_function=ereg_score_function,
        optimize_type=optimize_type,
        resolution=resolution,
        kp_range=kp_range,
        ki_range=ki_range,
        auto_range=auto_range
    ).run()


class _OptimizePIController:
    def __init__(
            self,
            *,
            tf_function: Callable[[float, float], Tuple[List[float], List[float]]],
            ta_score_function: Callable[[float], float] = _default_ta_score_function,
            s0_score_function: Callable[[float], float] = _default_s0_score_function,
            ereg_score_function: Callable[[float], float] = _default_ereg_score_function,
            optimize_type: str = 'dot_grid',

            resolution: float = 0.1,
            kp_range: Tuple[float, float] = None,
            ki_range: Tuple[float, float] = None,
            auto_range: bool = True,
    ):
        self.tf_function = tf_function
        self.ta_score_function = ta_score_function
        self.s0_score_function = s0_score_function
        self.ereg_score_function = ereg_score_function
        self.optimize_type = optimize_type
        self.resolution = resolution
        self.ki_range = ki_range
        self.kp_range = kp_range
        self.auto_range = auto_range

        if auto_range:
            self.auto_range_calculation()

    def auto_range_calculation(self):
        self.kp_range = [0, 10]
        self.ki_range = [0, 10]

    def enforce_optimize_type_params(self):
        if self.optimize_type == 'dot_grid':
            pass
        else:
            raise NotImplemented(f'unknown optimize option: {self.optimize_type}')

    def run(self):
        return {'dot_grid': self.dot_grid_optimize}.get(self.optimize_type)()

    def dot_grid_optimize(self):
        inkps = np.arange(*self.kp_range, self.resolution)
        inkis = np.arange(*self.ki_range, self.resolution)

        score = {}
        for kp in inkps:
            for ki in inkis:
                grf = control.step_response(control.tf(*self.tf_function(kp, ki)))
                s0 = max(grf[1]) - 1
                ereg = grf[1][-1] - 1

                ta = 10000000
                if ereg < 5/100:
                    for idx, val in zip(reversed(grf[0]), reversed(grf[1])):
                        if -5 > (val - 1) * 100 > 5:
                            ta = idx
                            break
                score[(kp, ki)] = ta, s0, ereg, self.calculate_score(ta, s0, ereg)
        return score

    def calculate_score(self, ta, s0, ereg):
        return sum((
            self.ta_score_function(ta),
            self.s0_score_function(s0),
            self.ereg_score_function(ereg),
        ))