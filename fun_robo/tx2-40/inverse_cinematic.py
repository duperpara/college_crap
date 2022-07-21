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
    theta = step.theta
    alpha = step.alpha
    a = step.a
    d = step.d

    return trigsimp(nsimplify(trigsimp(Matrix([
        [cos(theta), -cos(alpha) * sin(theta), sin(alpha) * sin(theta), a * cos(theta)],
        [sin(theta), cos(alpha) * cos(theta), -sin(alpha) * cos(theta), a * sin(theta)],
        [0, sin(alpha), cos(alpha), d],
        [0, 0, 0, 1],
    ]), tolerance=1e-4, rational=True)))


# def round_expr(ex, round_by=4, ):
#     ex2 = ex
#     for a in sympy.preorder_traversal(ex):
#         if isinstance(a, sympy.Float):
#             if a > 10**-round_by or a < -10**-round_by:
#                 ex2 = ex2.sub(a, round(a, round_by))
#             elif type(a) != int:
#                 ex2 = ex2.sub(a, 0)
#     return ex2
#
#
# def round_matrix(matrix:pd.DataFrame, round_by=4) -> pd.DataFrame:
#     return matrix.apply(lambda x: round_expr(x, round_by))


def get_tranformations(dhsteps: List[DHStep]) -> List[Matrix]:
    return [dhstep_to_matrix(step) for step in dhsteps]


def cinematic_decouple_solution_reduced_altered_di():
    transformations = get_tranformations(table_def('reduced_altered_di'))

    matr = Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    for transformation in transformations:
        for idx in range(transformation.rows):
            print(transformation.row(idx))
        print("----------")
        matr = matr * transformation
    print()
    for idx in range(matr.rows):
        print(matr.row(idx))
    print("----------")

    inv_cin_matr = Matrix([
        [0, 0, 0, Symbol('px')],
        [0, 0, 0, Symbol('py')],
        [0, 0, 0, Symbol('pz')],
        [0, 0, 0, 1],
    ])
    matr = nsimplify((matr - inv_cin_matr), tolerance=1e-4, rational=True)

    eq_system = [
        matr[0, 3],
        matr[1, 3],
        matr[2, 3]
    ]
    for eq in eq_system:
        print(eq)

    # ----- manual subs -----
    resolve_symbols = (t1, t2, t3) = sympy.symbols("θ1, θ2, θ3")
    px, py, pz = sympy.symbols("px, py, pz")
    # eq_system[0] = -px - 35 * sin(t1) + 225 * sin(t3) * cos(t2) * cos(t1) + 225 * cos(t1) * cos(t3) * sin(
    #     t2) + 225 * cos(t1) * sin(t2)
    # eq_system[1] = -py + 225 * sin(t1) * sin(t3) * cos(t2) + 225 * sin(t1) * cos(t3) * sin(t2) + 225 * sin(t1) * sin(
    #     t2) + 35 * cos(t1)
    # eq_system[2] = -pz - 225 * sin(t3) * sin(t2) + 225 * cos(t2) * cos(t3) + 225 * cos(t2) + 225
    #
    # # ----- manual simplify -----
    # eq_system[0] = -((px + 35 * sin(t1)) / 225) - cos(t1) * (sin(t2 + t3) + cos(t2))
    # eq_system[1] = -((py - 35 * cos(t1)) / 225) - sin(t1) * (sin(t2 + t3) + sin(t2))
    # eq_system[2] = -((pz - 225) / 225) + cos(t2 + t3) + cos(t2)

    print("----------------\n")
    for eq in eq_system:
        print(eq)

    # print(solvers.solve(eq_system[2], Symbol('θ2')))
    # RESULTS IN:
    eq_system.append(nsimplify(
        -t2 + 355 / 226 - 2 * atan((sqrt(
            -pz ** 2 * tan(t3 / 2) ** 4 - 2 * pz ** 2 * tan(t3 / 2) ** 2 - pz ** 2 + 450 * pz * tan(
                t3 / 2) ** 4 + 900 * pz * tan(t3 / 2) ** 2 + 450 * pz - 50625 * tan(t3 / 2) ** 4 + 101250 * tan(
                t3 / 2) ** 2 + 151875) - 450) * (cos(t3) + 1) / (2 * (-pz + 225 * sin(t3) + 225))),
        tolerance=1e-4, rational=True))
    print("----------------\n")
    for eq in eq_system:
        print(eq)

    # print(solvers.solve(eq_system, Symbol('θ3')))

    for solve_set in solvers.solve(eq_system, sympy.symbols('θ1')):
        print(solve_set)
        # for var, item in zip(['θ1', 'θ2', 'θ3'], solve_set):
        #     print(f"{var}: {item}")
        # print("----------------\n")
    # result_di = {symb: nsimplify(result, tolerance=1e-4, rational=True)
    #              for symb, result in zip(["θ1", "θ2", "θ3"], solvers.solve(eq_system, resolve_symbols))}
    # for key, value in result_di:
    #     print(f"{key}: {value}")

    input()


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
        # for idx in range(transformation.rows):
        #     print(transformation.row(idx))
        # print("----------")
        matr = matr * transformation
    # print()
    # for idx in range(matr.rows):
    #     print(matr.row(idx))
    # print("----------")

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
    print(get_transformations_and_eq_system())
    # cinematic_decouple_solution_reduced_altered_di()
