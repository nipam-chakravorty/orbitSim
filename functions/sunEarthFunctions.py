import numpy as np

# defining in terms of astronomical unit
GM = 4 * np.pi**2

# acceleration due to gravity
def accl(x, y):
    r3 = (np.sqrt(x*x + y*y))**3
    accl_x =  -GM * x / r3
    accl_y =  -GM * y / r3
    return accl_x, accl_y

# intial vx and vy are to be provided
def vel(vx, vy, accl_x, accl_y, t):
    vx_new = vx + accl_x*t
    vy_new = vy + accl_y*t
    return vx_new, vy_new

def posn(x, y, vx, vy, t):
    x_new = x + vx*t
    y_new = y + vy*t
    return x_new, y_new