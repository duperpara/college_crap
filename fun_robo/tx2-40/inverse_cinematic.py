from typing import List

import sympy
from IPython.core.display import display
from sympy import cos, sin, Matrix, nsimplify, Symbol, simplify, S, solvers, init_printing, pprint
import pandas as pd

from direct_cinematic import table_def, DHStep


def dhstep_to_matrix(step: DHStep) -> Matrix:
    theta = step.theta
    alpha = step.alpha
    a = step.a
    d = step.d

    return nsimplify(Matrix([
        [cos(theta), -cos(alpha) * sin(theta), sin(alpha) * sin(theta), a * cos(theta)],
        [sin(theta), cos(alpha) * cos(theta), -sin(alpha) * cos(theta), a * sin(theta)],
        [0, sin(alpha), cos(alpha), d],
        [0, 0, 0, 1],
    ]), tolerance=1e-4, rational=True)


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


def cinematic_decouple_solution():
    transformations = get_tranformations(table_def())

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
    eq_system[0] = -px - 35 * sin(t1) + 225 * sin(t3) * cos(t2) * cos(t1) + 225 * cos(t1) * cos(t3) * sin(
        t2) + 225 * cos(t1) * sin(t2)
    eq_system[1] = -py + 225 * sin(t1) * sin(t3) * cos(t2) + 225 * sin(t1) * cos(t3) * sin(t2) + 225 * sin(t1) * sin(
        t2) + 35 * cos(t1)
    eq_system[2] = -pz - 225 * sin(t3) * sin(t2) + 225 * cos(t2) * cos(t3) + 225 * cos(t2) + 225

    # ----- manual simplify -----
    eq_system[0] = -((px + 35 * sin(t1)) / 225) - cos(t1) * (sin(t2 + t3) + cos(t2))
    eq_system[1] = -((py - 35 * cos(t1)) / 225) - sin(t1) * (sin(t2 + t3) + sin(t2))
    eq_system[2] = -((pz - 225) / 225) + cos(t2 + t3) + cos(t2)

    print("----------------\n")
    for eq in eq_system:
        print(eq)

    print(solvers.solve(eq_system[2], Symbol('θ2')))

    for solve_set in solvers.solve(eq_system, resolve_symbols):
        print(solve_set)
        for var, item in zip(['θ1', 'θ2', 'θ3'], solve_set):
            print(f"{var}: {item}")
        print("----------------\n")
    # result_di = {symb: nsimplify(result, tolerance=1e-4, rational=True)
    #              for symb, result in zip(["θ1", "θ2", "θ3"], solvers.solve(eq_system, resolve_symbols))}
    # for key, value in result_di:
    #     print(f"{key}: {value}")

    input()
    inv_cin_matr = Matrix([
        [Symbol('nx'), Symbol('ox'), Symbol('ax'), Symbol('px')],
        [Symbol('ny'), Symbol('oy'), Symbol('ay'), Symbol('py')],
        [Symbol('nz'), Symbol('oz'), Symbol('az'), Symbol('pz')],
        [0, 0, 0, 1],
    ])
    resolve_symbols = [value for value in matr.values() if isinstance(value, sympy.core.symbol.Symbol)]

    eq_system = (matr - inv_cin_matr).values()
    eq_system = [simplify(eq) for eq in eq_system]
    for eq in eq_system:
        print(eq)

    # print(solvers.nonlinsolve(eq_system, sympy.symbols("θ1, θ2, θ3, θ4, θ5, θ6")))


if __name__ == '__main__':
    init_printing()
    cinematic_decouple_solution()
