import numpy as np

# defining in terms of astronomical unit
GM = 4 * np.pi**2

# acceleration due to gravity
def accl(x, y):
    r3 = (np.sqrt(x*x + y*y))**3
    accl_x =  -GM * x / r3
    accl_y =  -GM * y / r3
    return accl_x, accl_y

def RK4(x, y, vx, vy, t):

    ax, ay = accl(x, y)
    F1vx = t * ax
    F1vy = t * ay
    F1x = t * vx
    F1y = t * vy

    ax, ay = accl(x + 0.5*F1x, y + 0.5*F1y)
    F2vx = t * ax
    F2vy = t * ay
    F2x = t * (vx + 0.5*F1vx)
    F2y = t * (vy + 0.5*F1vy)

    ax, ay = accl(x + 0.5*F2x, y + 0.5*F2y)
    F3vx = t * ax
    F3vy = t * ay
    F3x = t * (vx + 0.5*F2vx)
    F3y = t * (vy + 0.5*F2vy)

    ax, ay = accl(x + F3x, y + F3y)
    F4vx = t * ax
    F4vy = t * ay
    F4x = t * (vx + F3vx)
    F4y = t * (vy + F3vy)

    x_new = x + (F1x + 2*F2x + 2*F3x + F4x)/6
    y_new = y + (F1y + 2*F2y + 2*F3y + F4y)/6

    vx_new = vx + (F1vx + 2*F2vx + 2*F3vx + F4vx)/6
    vy_new = vy + (F1vy + 2*F2vy + 2*F3vy + F4vy)/6

    return x_new, y_new, vx_new, vy_new