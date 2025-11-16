import numpy as np
from .parameters import a, b, c, h, f, nu_0, g_0
from scipy.linalg import LinAlgError
from .initial_conditions import y0

def cyc(i):
    return i, (i + 1) % 3, (i + 2) % 3


def G(y, i):
    i, j, k = cyc(i)
    g = y[i] - (2.0 * c**2 / a[i]) * y[j] * y[k]
    return g


def d(i, y, z):
    i, j, k = cyc(i)
    d = a[j] * a[k] * (
        c * (a[k] - a[j]) * y[j] * y[k]
        + c * a[i] * ((z[j] - h[j]) * y[k] - y[j] * (z[k] - h[k]))
        + a[i] * (nu_0 * a[i] * (z[i] - y[i]) - f[i])
    ) - 2.0 * c**2 * (
        c * a[j] * (a[j] - a[i]) * y[i] * y[j] ** 2
        + c * a[k] * (a[i] - a[k]) * y[i] * y[k] ** 2
        - nu_0 * a[j] * a[k] * (a[j] + a[k]) * y[j] * y[k]
    )
    return d


def Delta(i, y):
    i, j, k = cyc(i)
    delta = a[i] * a[j] * a[k] * (1.0 + g_0 * a[i]) - 2.0 * c**2 * (
        (a[j] ** 2) * b[j] * (y[j] ** 2) + (a[k] ** 2) * b[k] * (y[k] ** 2)
    )
    return delta


def Gamma(i, y, z):
    i, j, k = cyc(i)
    gamma = -(
        a[j]
        * a[k]
        * (y[k] * (2.0 * c**2 - a[k] * b[k]) + a[i] * b[k] * (z[k] - h[k]))
        + 2.0 * c**2 * a[i] * a[j] * b[i] * y[i] * y[j]
    )
    return gamma


def Sigma(i, y, z):
    i, j, k = cyc(i)
    sigma = -(
        a[j]
        * a[k]
        * (y[j] * (2.0 * c**2 - a[j] * b[j]) + a[i] * b[j] * (z[j] - h[j]))
        + 2.0 * c**2 * a[i] * a[k] * b[i] * y[i] * y[k]
    )
    return sigma


def M_matrix_from_z(y, z):
    M = np.zeros((3, 3), dtype=float)
    M[0, 0] = Delta(0, y)
    M[0, 1] = Gamma(0, y, z)
    M[0, 2] = Sigma(0, y, z)
    M[1, 0] = Sigma(1, y, z)
    M[1, 1] = Delta(1, y)
    M[1, 2] = Gamma(1, y, z)
    M[2, 0] = Gamma(2, y, z)
    M[2, 1] = Sigma(2, y, z)
    M[2, 2] = Delta(2, y)
    return M


def Phi(y):
    z = np.array([G(y0, i) for i in range(3)], dtype=float)
    dvec = np.array([d(i, y0, z) for i in range(3)], dtype=float)

    M = M_matrix_from_z(y0, z)
    try:
        M_inv = np.linalg.inv(M)
        phi_vec = M_inv @ dvec
    except np.linalg.LinAlgError:
        print("Singular matrix found. Using pseudo-inverse.")
        phi_vec = np.linalg.pinv(M) @ dvec

    return phi_vec
