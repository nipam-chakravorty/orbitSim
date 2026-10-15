# upgrade to RK4
# reduce the time step

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

#m_E = 1                                                         # all mass to be taken multiple of earth mass
GM = 4*np.pi**2                                                  # taking G as 1

x = 1                                                           # 1 AU
y = 0                                                           # y coordinate as 0

#M = 10*m_E                                                      # mass of sun

vy = np.sqrt(GM/x)
vx = 0                                                          # velocity at (1,0)

def accl(x, y):
    r3 = (np.sqrt(x*x + y*y))**3
    accl_x =  -GM * x / r3
    accl_y =  -GM * y / r3
    return accl_x, accl_y

def vel(x, y, vx, vy, accl_x, accl_y, t):
    vx_new = vx + accl_x*t
    vy_new = vy + accl_y*t
    return vx_new, vy_new

def posn(x, y, vx, vy, t):

    x_new = x + vx*t
    y_new = y + vy*t

    return x_new, y_new

positions = []

dt = 0.1

for _ in np.arange(200):

    ax, ay = accl(x, y)
    vx, vy = vel(x, y, vx, vy, ax, ay, dt)
    x, y = posn(x, y, vx, vy, dt)

    positions.append([x, y])

positions = np.array(positions)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("Sun and Earch")
ax.plot(0, 0, "yo", markersize=15)            # the "sun" at the origin

planet, = ax.plot([], [], "bo", markersize=8)  # current position
trail,  = ax.plot([], [], "b-", alpha=0.4)     # path so far

def update(frame):
    planet.set_data([positions[frame, 0]], [positions[frame, 1]])
    trail.set_data(positions[:frame+1, 0], positions[:frame+1, 1])
    return planet, trail

anim = FuncAnimation(fig, update, frames=len(positions), interval=20, blit=True)

anim.save("sunEarth.webp", writer=PillowWriter(fps=30), dpi=100)

plt.show()