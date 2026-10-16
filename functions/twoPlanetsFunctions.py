import numpy as np

# initial postions (x1, y1) and (x2, y2), are to be user inputted
def accl(x1, y1, x2, y2,  GM, Gm1, Gm2):
    dx = x2 - x1
    dy = y2 - y1
    d3 = (dx*dx + dy*dy)**(1.5)
    r3_1 = (x1*x1 + y1*y1)**(1.5)
    r3_2 = (x2*x2 + y2*y2)**(1.5)

    a1x = - (GM * x1)/r3_1 + (Gm2 * dx)/d3
    a1y = - (GM * y1)/r3_1 + (Gm2 * dy)/d3

    a2x = - (GM * x2)/r3_2 - (Gm1 * dx)/d3
    a2y = - (GM * y2)/r3_2 - (Gm2 * dy)/d3

    return a1x, a1y, a2x, a2y


# initial velocities (v1x, v1y) and (v2x, v2y) are to be user inputted
def vel(v1x, v1y, v2x, v2y, a1x, a1y, a2x, a2y, t):
    v1x_new = v1x + a1x*t
    v1y_new = v1y + a1y*t

    v2x_new = v2x + a2x*t
    v2y_new = v2y + a2y*t

    return v1x_new, v1y_new, v2x_new, v2y_new

# updating postions
def posn(x1, y1, x2, y2, v1x, v1y, v2x, v2y, t):
    x1_new = x1 + v1x*t
    y1_new = y1 + v1y*t
    x2_new = x2 + v2x*t
    y2_new = y2 + v2y*t

    return x1_new, y1_new, x2_new, y2_new