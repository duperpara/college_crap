from typing import List

import sympy
from sympy import cos, sin, Matrix, nsimplify, Symbol, simplify, S, solvers, init_printing, pprint, atan, sqrt, tan, \
    acos, trigsimp
import pandas as pd

from direct_cinematic import table_def, DHStep

import collections

from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support


def dhstep_to_matrix(step: DHStep) -> Matrix:
    theta = trigsimp(step.theta)
    alpha = trigsimp(step.alpha)
    a = trigsimp(step.a)
    d = trigsimp(step.d)

    return Matrix([
        [cos(theta), -cos(alpha) * sin(theta), sin(alpha) * sin(theta), a * cos(theta)],
        [sin(theta), cos(alpha) * cos(theta), -sin(alpha) * cos(theta), a * sin(theta)],
        [0, sin(alpha), cos(alpha), d],
        [0, 0, 0, 1],
    ]).applyfunc(trigsimp)


def round_mul(mul: sympy.Mul, round_by=4):
    print(f"{mul = }")
    # mul2 = mul.copy()
    for a in sympy.preorder_traversal(mul):
        print(f"{a = }")
    mul = mul.evalf(n=round_by)
    print(sympy.Expr(mul))
    print(f"{mul = }\n")
    return mul


def round_expr(ex, round_by=4):
    if isinstance(ex, sympy.Mul):
        ex = sympy.Expr(ex)
    ex2 = ex
    for a in sympy.preorder_traversal(ex):
        if isinstance(a, sympy.Float):
            if a > 10**-round_by or a < -10**-round_by:
                ex2 = ex2.subs(a, round(a, round_by))
            elif type(a) != int:
                ex2 = ex2.subs(a, 0)
    return sympy.Mul(ex2)

#
#
# def round_matrix(matrix:pd.DataFrame, round_by=4) -> pd.DataFrame:
#     return matrix.apply(lambda x: round_expr(x, round_by))


def get_tranformations(dhsteps: List[DHStep]) -> List[Matrix]:
    return [dhstep_to_matrix(step) for step in dhsteps]


def cinematic_decouple_solution_reduced_altered_di():
    di = {}

    transformations = get_tranformations(table_def('reduced_altered_di'))
    di['transformations'] = transformations

    matr = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    for transformation in transformations:
        matr = matr * transformation
    matr = matr.applyfunc(trigsimp)

    di["tot_transf"] = matr

    inv_cin_matr = Matrix([
        [0, 0, 0, Symbol('px')],
        [0, 0, 0, Symbol('py')],
        [0, 0, 0, Symbol('pz')],
        [0, 0, 0, 1],
    ])

    eq_system = trigsimp((matr - inv_cin_matr)).values()
    di['eq_system'] = eq_system

    return di


def get_transformations_and_eq_system():
    di = {}

    transformations = get_tranformations(table_def())
    di['transformations'] = transformations

    matr = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    for transformation in transformations:
        matr = matr * transformation
    matr = matr.applyfunc(trigsimp)

    di["tot_transf"] = matr

    inv_cin_matr = Matrix([
        [Symbol('nx'), Symbol('ox'), Symbol('ax'), Symbol('px')],
        [Symbol('ny'), Symbol('oy'), Symbol('ay'), Symbol('py')],
        [Symbol('nz'), Symbol('oz'), Symbol('az'), Symbol('pz')],
        [0, 0, 0, 1],
    ])

    eq_system = trigsimp(nsimplify(trigsimp((matr - inv_cin_matr), tolerance=1e-4, rational=True))).values()

    di['eq_system'] = eq_system
    return di
    # eq_str_li = []
    # symb_di_li = []
    # for eq in eq_system:
    #     print(eq)
    #     eq_str_li.append(str(eq))
    #     print(dict(sorted({str(symb): eq.count(symb) for symb in eq.free_symbols}.items())))
    #     symb_di_li.append(dict(sorted({str(symb): eq.count(symb) for symb in eq.free_symbols}.items())))
    #     print('_-_-_-_-_-_-_-_-_-_\n')
    #
    # print(eq_str_li)
    # print(symb_di_li)

    # # ----- manual subs -----
    # resolve_symbols = (t1, t2, t3, t4, t5, t6) = sympy.symbols("θ1, θ2, θ3, θ4, θ5, θ6")
    # az, px, py, pz = sympy.symbols("az, px, py, pz")
    #
    # az_eq = nsimplify(eq_system[-2], tolerance=1e-4, rational=True)
    # pz_eq = nsimplify(eq_system[-1], tolerance=1e-4, rational=True)
    #
    # print(az_eq)
    # print(dict(sorted({str(symb): az_eq.count(symb) for symb in az_eq.free_symbols}.items())))
    # solve = solvers.solve(az_eq, sympy.symbols("θ4"))
    # az_sol = solve[1]
    # print(az_sol)
    # print(dict(sorted({str(symb): az_sol.count(symb) for symb in az_sol.free_symbols}.items())))
    #
    # print(pz_eq)
    # print(dict(sorted({str(symb): pz_eq.count(symb) for symb in pz_eq.free_symbols}.items())))
    # solve = solvers.solve(pz_eq, sympy.symbols("θ4"))
    # pz_sol = solve[1]
    # print(pz_sol)
    # print(dict(sorted({str(symb): pz_sol.count(symb) for symb in pz_sol.free_symbols}.items())))
    #
    # print('_-_-_-_-_-_-_-_-_-_\n')
    #
    # eq = nsimplify(az_sol - pz_sol)
    # print(eq)
    # # eq = ((-az + cos(t5) * cos(t2 + t3)) / (sin(t5) * sin(t2 + t3))) - \
    # #      ((-pz + 225 * cos(t2) + 65 * cos(t5) * cos(t2 + t3) + 225 * cos(t2 + t3) + 225) / (
    # #                  65 * sin(t5) * sin(t2 + t3)))
    # # print(eq)
    # print(solvers.solve(eq, Symbol("θ5")))
    #
    # manual_sol = acos(((((-pz / 225) + 65 * az + cos(t2) + 1) / cos(t2 + t3)) - 1) / (65 - (65 / 225)))
    # print(nsimplify(manual_sol, tolerance=1e-4, rational=True))
    # # print(solvers.checksol(eq, t5, manual_sol))
    #
    # ax_eq = nsimplify(eq_system[2], tolerance=1e-4, rational=True)
    # ay_eq = nsimplify(eq_system[6], tolerance=1e-4, rational=True)
    #
    # print(ax_eq)
    # print(dict(sorted({str(symb): ax_eq.count(symb) for symb in ax_eq.free_symbols}.items())))
    #
    # print(ay_eq)
    # print(dict(sorted({str(symb): ax_eq.count(symb) for symb in ax_eq.free_symbols}.items())))
    #
    # eq = nsimplify(ax_eq - ay_eq, tolerance=1e-4, rational=True)
    # print(eq)
    # print(dict(sorted({str(symb): eq.count(symb) for symb in eq.free_symbols}.items())))


    # print(solvers.solve(ax_eq, t1))
    # print(solvers.solve(ay_eq, t1))







    # tupli = [
    #     (eq_system, t1),
    #     (eq_system, t2),
    #     (eq_system, t3),
    #     (eq_system, t4),
    #     (eq_system, t5),
    #     (eq_system, t6),
    # ]
    # with Pool(processes=6) as pool:
    #     pool.starmap(print_solve, tupli)

    # print(solvers.nonlinsolve(eq_system, *resolve_symbols))


def print_solve(*args, **kwargs):
    print(solvers.solve(*args, **kwargs))


if __name__ == '__main__':
    # print(get_transformations_and_eq_system())
    cinematic_decouple_solution_reduced_altered_di()
