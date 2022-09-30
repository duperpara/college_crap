import math

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
        'h, A, dt, U, K, a, g, ro, Ve, Vs, v, pf, c1, c2, h0, U0')
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
    eq_statements['tf'] = Eq(
        Delta_h / Delta_U, Ke / (tau * s + 1)
    )


    for name, eq in eq_statements.items():
        print(f'{name}: {eq}')
    return eq_statements


def evaluate_tf_constants(equations: dict, *, h0, a, A, K, g=9.806):
    alpha, tau, Ke, h0_var, a_var, A_var, K_var, g_var = symbols('alpha, tau, Ke, h0, a, A, K, g')
    subs_dict = {
        h0_var: h0,
        a_var: a,
        A_var: A,
        K_var: K,
        g_var: g
    }

    def make_subs(eq):
        for var, val in subs_dict.items():
            eq = eq.subs(var, val)
        return eq
    alpha_val = make_subs(equations.get('alpha_subs').right_side)
    subs_dict[alpha] = alpha_val

    tau_val = make_subs(equations.get('tau_subs').right_side)
    subs_dict[tau] = tau_val

    Ke_val = make_subs(equations.get('Ke_subs').right_side)
    subs_dict[Ke] = Ke_val

    return make_subs(equations.get('tf').right_side).subs(sqrt(2), math.sqrt(2))


if __name__ == '__main__':
    run()
