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
    h, A, dt, U, K, a, g, ro, Ve, Vs, v, pf, c1, c2, h0, U0 = symbols(
        'h, A, dt, U, K, a, g, ro, Ve, Vs, v, pf, c1, c2, h0, U0',
        real=True, positive=True)
    d, H, Ul, s, Delta_h, Delta_U, alpha, tau, Ke = symbols('d, H, Ul, s, Delta_h, Delta_U, alpha, tau, Ke')

    eq_statements = {}
    eq_statements['dhdt_flow'] = (Eq(
        d * h / dt,
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
    eq_statements['dhdt_flow_detailed'] = (Eq(
        d * h / dt,
        (eq_statements.get('in_flow').right_side - eq_statements.get('out_flow2').right_side) / A
    ))
    eq_statements['h_subs'] = (Eq(
        h, h0 + Delta_h
    ))
    eq_statements['U_subs'] = (Eq(
        U, U0 + Delta_U
    ))
    eq_statements['delta_flow_detailed'] = Eq(
        eq_statements.get('dhdt_flow_detailed').left_side.subs(h, eq_statements.get('h_subs').right_side),
        eq_statements.get('dhdt_flow_detailed').right_side.subs(h, eq_statements.get('h_subs').right_side
                                                                ).subs(U, eq_statements.get('U_subs').right_side),
    )
    eq_statements['equilibrium'] = Eq(
        K*U0, a*sqrt(2*g*h0)
    )
    eq_statements['linearize'] = Eq(
        A * (d * Delta_h) / dt, K * U0 + K * Delta_U - a * sqrt(2 * g * h0) - a * sqrt(2 * g) * Delta_h / (2 * sqrt(h0))
    )
    eq_statements['linearize_equilibrium'] = Eq(
        eq_statements.get('linearize').left_side, K * Delta_U - Delta_h * (a * sqrt(2 * g) / (2 * sqrt(h0)))
    )
    eq_statements['alpha_subs'] = Eq(
        alpha, (a*sqrt(2*g)/(2*sqrt(h0)))
    )
    eq_statements['linearize_equilibrium_alpha_subs'] = Eq(
        eq_statements['linearize_equilibrium'].left_side, eq_statements['linearize_equilibrium'].right_side.subs(
            eq_statements['alpha_subs'].right_side, eq_statements['alpha_subs'].left_side
        )
    )
    eq_statements['laplace_transform'] = Eq(
        s * A * Delta_h, K * Delta_U - alpha * Delta_h
    )
    eq_statements['tau_subs'] = Eq(
        tau, A/alpha
    )
    eq_statements['Ke_subs'] = Eq(
        Ke, K/alpha
    )
    eq_statements['laplace_tau_Ke_subs_simplify'] = Eq(
        Delta_h, Ke * Delta_U / (tau * s + 1)
    )

    # taylor_funs = h_linearize(0, 180, [0.2, 0.4, 0.6, 0.8, 1], h, sqrt(h))
    # eq_statements['sqrt_h_linearization'] = (Eq(
    #     sqrt(h),
    #     taylor_funs[2]
    # ))
    # eq_statements['dhdt_flow_detailed2'] = (Eq(
    #     dh / dt,
    #     (eq_statements.get('in_flow').right_side
    #      - eq_statements.get('out_flow2').right_side.subs(sqrt(h), eq_statements.get('sqrt_h_linearization').right_side)
    #      )/A
    # ))
    # eq_statements['dhdt_flow_laplace'] = (Eq(
    #     H*s,
    #     ((eq_statements.get('in_flow').right_side
    #      - eq_statements.get('out_flow2').right_side.subs(sqrt(h), eq_statements.get('sqrt_h_linearization').right_side)
    #      )/A).subs(h, H*s).subs(U, Ul*s)
    # ))
    # eq_statements['dhdt_flow_laplace'] = (Eq(
    #     c1*h + c2,
    #     taylor_funs[2]
    # ))
    # eq_statements['dhdt_flow_laplace2'] = (Eq(
    #     H,
    #     K*Ul/(A-sqrt(2*g)*a*c1) - (1/s)*(sqrt(2*g)*a*c2/(A-sqrt(2*g)*a*c1))
    # ))

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
