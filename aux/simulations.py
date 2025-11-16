import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from .phi import Phi
from .parameters import a, b, c, h, f, nu_0, kappa_0, g_0

TIMESCALE_FACTOR = 8.0

def cyc(i):
    return i, (i + 1) % 3, (i + 2) % 3


def cyc(i):
    return i, (i + 1) % 3, (i + 2) % 3

def pe_model(t, u):

    x = u[0:3]
    y = u[3:6]
    z = u[6:9]
    dx = np.zeros(3)
    dy = np.zeros(3)
    dz = np.zeros(3)

    for i in range(3):
        i_, j, k = cyc(i)
        dx[i] = (
            a[i] * b[i] * x[j] * x[k]
            - c * (a[i] - a[k]) * x[j] * y[k]
            + c * (a[i] - a[j]) * y[j] * x[k]
            - 2 * c**2 * y[j] * y[k]
            - nu_0 * (a[i] ** 2) * x[i]
            + a[i] * y[i]
            - a[i] * z[i]
        ) / a[i]
        dy[i] = (
            -a[k] * b[k] * x[j] * y[k]
            - a[j] * b[j] * y[j] * x[k]
            + c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * x[i]
            - nu_0 * (a[i] ** 2) * y[i]
        ) / a[i]
        dz[i] = (
            -b[k] * x[j] * (z[k] - h[k])
            - b[j] * (z[j] - h[j]) * x[k]
            + c * y[j] * (z[k] - h[k])
            - c * (z[j] - h[j]) * y[k]
            + g_0 * a[i] * x[i]
            - kappa_0 * a[i] * z[i]
            + f[i]
        )
    return np.concatenate([dx, dy, dz])


def pe_simulate(x0, y0, z0, days):
    initial_u = np.concatenate([x0, y0, z0])
    t_final = days * TIMESCALE_FACTOR
    t_span = (0.0, t_final)

    print("Starting numerical integration for PE model...")
    sol = solve_ivp(pe_model, t_span, initial_u, method="RK45", atol=1e-8, rtol=1e-6)
    print("Please wait...")

    t_out = sol.t / TIMESCALE_FACTOR
    x, y, z = sol.y[0:3].T, sol.y[3:6].T, sol.y[6:9].T

    df = pd.DataFrame({
        "time": t_out,
        "x1": x[:, 0], "x2": x[:, 1], "x3": x[:, 2],
        "y1": y[:, 0], "y2": y[:, 1], "y3": y[:, 2],
        "z1": z[:, 0], "z2": z[:, 1], "z3": z[:, 2],
    })
    return df

def be_model(tau, y, phi_vec):
    dydt = np.zeros(3, dtype=float)
    for i in range(3):
        i_, j, k = cyc(i)
        dydt[i] = (
            - (a[k] * b[k] / a[i]) * phi_vec[j] * y[k]
            - (a[j] * b[j] / a[i]) * y[j] * phi_vec[k]
            + (c * (a[k] - a[j]) / a[i]) * y[j] * y[k]
            - phi_vec[i]
            - nu_0 * a[i] * y[i]
        )
    return dydt

def qg_model(t, y):
    dy = np.zeros(3, dtype=float)
    for i in range(3):
        _, j, k = cyc(i)
        dy[i] = (
            g_0 * c * (a[k] - a[j]) * y[j] * y[k]
            - a[i] * (a[i] * g_0 * nu_0 + kappa_0) * y[i]
            - c * h[k] * y[j]
            + c * h[j] * y[k]
            + f[i]
        ) / (a[i] * g_0 + 1.0)
    return dy

def simulate_model(model_func, y0, days, model_name, dt=0.001, model_args=()):
    t_final = days * TIMESCALE_FACTOR
    t_span = (0, t_final)
    t_eval = np.arange(0, t_final + dt, dt)

    print(f"Starting numerical integration for {model_name} model...")
    sol = solve_ivp(
        model_func, t_span, y0, t_eval=t_eval, args=model_args,
        method="RK45", atol=1e-8, rtol=1e-6
    )
    print("Please wait...")

    t = sol.t / TIMESCALE_FACTOR
    y = sol.y

    df = pd.DataFrame({
        "time": t,
        "y1": y[0], "y2": y[1], "y3": y[2],
    })
    return df

def be_simulate(y0, days):
    phi_vec = Phi(y0)
    return simulate_model(be_model, y0, days, "BE", model_args=(phi_vec,))

def qg_simulate(y0, days):
    return simulate_model(qg_model, y0, days, "QG")