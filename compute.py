import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import pylab as pl
import os, time, glob

def func(x):
    return pow(x,2)

def alpha_A(K):
    return -27.664 + 3278 * K
def alpha_As(K):
    return 0.001472 + 0.003807 * K
def alpha_Bs(K):
    return 0.0004755 + 0.001237 * K
def alpha_An(K):
    return -0.707 + 7759 * K
def alpha_Bn(K):
    return 306.954 + 5585 * K

def beta_A():
    return 0.43
def beta_As():
    return 1.59
def beta_Bs():
    return 1.81
def beta_An():
    return -1.36
def beta_Bn():
    return -1.4

def A_d(d, K):
    return alpha_A(K) * math.pow(d, beta_A())
def A_nd(d, K):
    return alpha_An(K) * math.pow(d, beta_An())
def B_nd(d, K):
    return alpha_Bn(K) * math.pow(d, beta_Bn())
def A_sd(d, K):
    return alpha_As(K) * math.pow(d, beta_As())
def B_sd(d, K):
    return alpha_Bs(K) * math.pow(d, beta_Bs())

def Xmin(d, K):
    return round(max(A_nd(d, K) - B_nd(d, K) * np.sqrt(np.log(10)), 1e-15) / 100.0) * 100.0

def Xmax(d, K):
    return round(max(A_nd(d, K) + B_nd(d, K) * np.sqrt(np.log(10)), 1e-15) / 100.0) * 100.0

def Ymin(d, K):
    return round(max(A_sd(d, K) - B_sd(d, K) * np.sqrt(np.log(10)), 1e-15) / 100.0) * 100.0

def Ymax(d, K):
    return round(max(A_sd(d, K) + B_sd(d, K) * np.sqrt(np.log(10)), 1e-15) / 100.0) * 100.0

def Xmax_(xmax, xmin):
    return xmax + (xmax - xmin) / 2.0

def Xmin_(xmax, xmin):
    return max(1e-15,(xmax - (xmax - xmin) / 2.0))

def V(n, d):
    return np.pi * d * n / 1000 

def S(n, d, K):
    return (A_sd(d, K) * B_nd(d, K) + np.sqrt((A_sd(d, K) * B_nd(d, K)) * (A_sd(d, K) * B_nd(d, K)) - 4.0 * B_sd(d, K) * B_sd(d, K) * A_nd(d, K) * n + 4.0 * B_sd(d, K) * B_sd(d, K) * n * n)) / (2.0 * B_nd(d, K))

def Sm(n, d, K):
    return S(n, d, K) * n

def L(n, S, d, K):
    return A_d(d, K) * np.exp(-((n - A_nd(d, K)) / B_nd(d, K)) * ((n - A_nd(d, K)) / B_nd(d, K)) - ((S - A_sd(d, K)) / B_sd(d, K)) * ((S - A_sd(d, K)) / B_sd(d, K)))

def Q(n, S, d, K, ec, el, q1, q2, q3):
    C = (ec.L0.data * ec.LC.data) * ec.c_u.data
    D = (ec.L0.data * ec.LC.data) * (ec.c_u.data * ec.t_u.data + ec.c_p.data / ec.k_s.data + ec.c_z.data * ec.t_z.data)
    N_toch = el.N_z.data / 60.0
    N_st = el.N_o.data / 60.0 + q3 * 73.7 * 0.00001 * math.pow(np.pi, 0.85) * math.pow(d, 1.75) * math.pow(n, 0.85) * math.pow(S, 0.8) * 1.2
    return q1*((ec.L0.data * ec.LC.data) / n / S * N_st + (ec.L0.data * ec.LC.data) / L(n, S, d, K) * (ec.k_s.data - 1) / ec.k_s.data * N_toch * ec.t_z.data) * el.N_p.data + q2 * (C / (S * n) + D / L(n, S, d, K))

def GSS_grid(num, minmax, d, K, ec, el, q1, q2, q3):
    return round((GSS(num, minmax, d, K, ec, el, q1, q2, q3) - Xmin_(Xmax(d, K), Xmin(d, K))) / (Xmax_(Xmax(d, K), Xmin(d, K)) - Xmin_(Xmax(d, K), Xmin(d, K))) * 800)

def GSS(num, minmax, d, K, ec, el, q1, q2, q3):
    a = float(Xmin(d, K))
    b = float(Xmax(d, K))
    phi = (1 + np.sqrt(5.0)) / 2.0
    eps = 0.001

    while (abs(b - a) > eps):
        x1 = b - ((b - a)/phi)
        x2 = a + ((b - a)/phi)
        if (num == 0):
            y1 = L(x1, S(x1, d, K), d, K)
            y2 = L(x2, S(x2, d, K), d, K)
        else:
            y1 = Q(x1, S(x1, d, K), d, K, ec, el, q1, q2, q3)
            y2 = Q(x2, S(x2, d, K), d, K, ec, el, q1, q2, q3)
        if (minmax == 0 and y1 >= y2) or (minmax == 1 and y1 <= y2):
            a = x1
        else:
            b = x2       
    return (a + b) / 2.0

def T(Lp, Smp):
    return Lp / Smp

def Graphic_L(n, So, d, K, Z, ec, el, q1, q2, q3):
    xmax = Xmax(d, K)

    x = np.arange(0.0, xmax * 1.2, 0.125)
    y = np.arange(0.02, S(Xmax(d, K) * 1.2, d,  K), 0.0025)
    xgrid, ygrid = np.meshgrid(x, y)

    zgrid = L(xgrid, ygrid, d, K)

    maxt = GSS(0, 1, d, K, ec, el, q1, q2, q3)
    xmin = A_d(d, K) / 10.0
    xmax = L(maxt, S(maxt, d, K), d, K)

    levels = []
    for i in range(0, Z):
        levels.append(((xmax - xmin) * (i + 1)/(Z + 1)) + xmin)
    
    cs = pl.contour(xgrid, ygrid, zgrid, levels, colors='#ff8000')
    pl.clabel(cs, inline=False, colors='red')
    pl.grid(True)
    
    return cs

def Graphic_Q(Qo, So, d, K, Z, ec, el, q1, q2, q3):
    xmax = Xmax(d, K)
    xmin = Qo
    x = np.arange(0.0, xmax * 1.2, 1.25)
    y = np.arange(0.02, S(xmax * 1.2, d,  K), 0.005)
    xgrid, ygrid = np.meshgrid(x, y)

    zgrid = np.array([Q(xx, yy, d, K, ec, el, q1, q2, q3) for xx, yy in zip(np.ravel(xgrid), np.ravel(ygrid))]).reshape(xgrid.shape)
    maxt = GSS(0, 1, d, K, ec, el, q1, q2, q3)
    mint = GSS(1, 0, d, K, ec, el, q1, q2, q3)
    xmax = Q(maxt, S(maxt, d, K), d, K, ec, el, q1, q2, q3)
    xmin = Q(mint, S(mint, d, K), d, K, ec, el, q1, q2, q3)
    levels = []
    for i in range(0, Z):
        levels.append(((xmax - xmin) * (i + 1)/(Z + 1)) + xmin)
    
    cs = pl.contour(xgrid, ygrid, zgrid, levels, colors='#0180b4')
    pl.clabel(cs, inline=False, colors='#005978')
    pl.grid(True)
    
    return cs

def N_opt(d, K, ec, el, q1, q2, q3):
    return GSS(0, 1, d, K, ec, el, q1, q2, q3)

def N_max(d, K, ec, el, q1, q2, q3):
    return GSS(1, 0, d, K, ec, el, q1, q2, q3)

if __name__ == '__main__':
    print(0)