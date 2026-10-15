import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# input parameters
Gm1 = 1
Gm2 = 318
GM  = 330000

x1 = 1
x2 = 5.2
y1 = 0
y2 = 0

# not input parameters

r1 = np.sqrt(x1*x1 + x2*x2)
r2 = np.sqrt(x2*x2 + y2*y2)

v1x = 0
v1y = np.sqrt((2*GM/x1)+(2*Gm2/(x2-x1)))
v2x = 0
v2y = np.sqrt((2*GM/x2)+(2*Gm1/(x2-x1)))

def accl(x1, y1, x2, y2):
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

def vel(x1, y1, x2, y2, a1x, a1y, a2x, a2y, t):
    v1x_new = v1x + a1x*t
    v1y_new = v1y + a1y*t

    v2x_new = v2x + a2x*t
    v2y_new = v2y + a2y*t

    return v1x_new, v1y_new, v2x_new, v2y_new

def posn(x1, y1, x2, y2, v1x, v1y, v2x, v2y, t):
    x1_new = x1 + v1x*t
    y1_new = y1 + v1y*t
    x2_new = x2 + v2x*t
    y2_new = y2 + v2y*t

    return x1_new, y1_new, x2_new, y2_new

positions = []

dt = 0.1

for t in np.arange(200):
    a1x, a1y, a2x, a2y = accl(x1, y1, x2, y2)
    v1x, v1y, v2x, v2y = vel(x1, y1, x2, y2, a1x, a1y, a2x, a2y, dt)
    x1, y1, x2, y2 = posn(x1, y1, x2, y2, v1x, v1y, v2x, v2y, dt)
    positions.append([x1, y1, x2, y2])
positions=np.array(positions)

positions = np.array(positions)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.set_xlim(-100000, 100000)
ax.set_ylim(-100000, 100000)
ax.set_title("3 body system")
ax.plot(0, 0, "yo", markersize=15)             # the "sun" at the origin

planet1, = ax.plot([], [], "bo", markersize=8)  # planet 1 current position
trail1,  = ax.plot([], [], "b-", alpha=0.4)     # planet 1 path so far

planet2, = ax.plot([], [], "ro", markersize=8)  # planet 2 current position
trail2,  = ax.plot([], [], "r-", alpha=0.4)     # planet 2 path so far

def update(frame):
    planet1.set_data([positions[frame, 0]], [positions[frame, 1]])
    trail1.set_data(positions[:frame+1, 0], positions[:frame+1, 1])

    planet2.set_data([positions[frame, 2]], [positions[frame, 3]])
    trail2.set_data(positions[:frame+1, 2], positions[:frame+1, 3])

    return planet1, trail1, planet2, trail2

anim = FuncAnimation(fig, update, frames=len(positions), interval=20, blit=True)

anim.save("3body.webp", writer=PillowWriter(fps=30), dpi=100)

plt.show()