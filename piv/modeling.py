from sympy import Symbol, sqrt, solve, derive_by_array, symbols


def run():
    eq_statements = flow_rate_equations()


class Eq:
    def __init__(self, left_side, right_side):
        self.left_side = left_side
        self.right_side = right_side

    def __repr__(self):
        return f"{self.left_side} = {self.right_side}"


def flow_rate_equations():
    h, A, dt, U, K, a, g, ro, Ve, Vs, v, pf, c1, c2 = symbols('h, A, dt, U, K, a, g, ro, Ve, Vs, v, pf, c1, c2',
                                                      real=True, positive=True)
    dh, H, Ul, s = symbols('dh, H, Ul, s')


    eq_statements = {}
    eq_statements['dhdt_flow'] = (Eq(
        dh / dt,
        (Ve - Vs) / A
    ))
    eq_statements['in_flow'] = (Eq(
        Ve,
        U * K
    ))
    eq_statements['out_flow1'] = (Eq(
        Vs,
        v * a
    ))
    eq_statements['out_flow2'] = (Eq(
        Vs,
        a * sqrt(2 * g) * sqrt(h)
    ))
    eq_statements['out_flow3'] = (Eq(
        Vs,
        a * sqrt(2 * g) * sqrt(pf / (ro * g))
    ))
    eq_statements['dhdt_flow_detailed1'] = (Eq(
        dh / dt,
        (eq_statements.get('in_flow').right_side - eq_statements.get('out_flow2').right_side)/A
    ))
    taylor_funs = h_linearize(0, 180, [0.2, 0.4, 0.6, 0.8, 1], h, sqrt(h))
    eq_statements['sqrt_h_linearization'] = (Eq(
        sqrt(h),
        taylor_funs[2]
    ))
    eq_statements['dhdt_flow_detailed2'] = (Eq(
        dh / dt,
        (eq_statements.get('in_flow').right_side
         - eq_statements.get('out_flow2').right_side.subs(sqrt(h), eq_statements.get('sqrt_h_linearization').right_side)
         )/A
    ))
    eq_statements['dhdt_flow_laplace'] = (Eq(
        H*s,
        ((eq_statements.get('in_flow').right_side
         - eq_statements.get('out_flow2').right_side.subs(sqrt(h), eq_statements.get('sqrt_h_linearization').right_side)
         )/A).subs(h, H*s).subs(U, Ul*s)
    ))
    eq_statements['dhdt_flow_laplace'] = (Eq(
        c1*h + c2,
        taylor_funs[2]
    ))
    eq_statements['dhdt_flow_laplace2'] = (Eq(
        H,
        K*Ul/(A-sqrt(2*g)*a*c1) - (1/s)*(sqrt(2*g)*a*c2/(A-sqrt(2*g)*a*c1))
    ))

    for name, eq in eq_statements.items():
        print(f'{name}: {eq}')
    return eq_statements


def h_linearize(min_height, max_height, taylor_range, h, h_fun):
    print(h_fun)
    delta_h = max_height - min_height
    taylor_targets = [min_height + (delta_h * p) for p in taylor_range]
    print(f"{taylor_targets = }")

    taylor_funs = []
    for taylor_target in taylor_targets:
        expr_1 = h_fun.subs(h, taylor_target)
        expr_2 = derive_by_array(h_fun, h).subs(h, taylor_target) * (h - taylor_target)
        # print(f'{expr_1 = }')
        # print(f'{expr_2 = }')

        taylor_fun = expr_1 + expr_2
        # print(f'{taylor_fun = }')
        taylor_funs.append(taylor_fun)

    # print(taylor_funs)
    return taylor_funs


if __name__ == '__main__':
    run()
