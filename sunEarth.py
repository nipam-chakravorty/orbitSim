# upgrade to RK4
# reduce the time step

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from functions import sunEarthFunctions as sef

# defining in terms of astronomical unit, M is the mass of the sun
# already have been defined in the functions
# can be imported as well if not modifing
GM = 4*np.pi**2                                            

# defining initial positons
x = 1                                                          
y = 0                                                          

# defining initial velocity
vy = np.sqrt(GM/x)
vx = 0

positions = []

dt = 0.1

for _ in np.arange(200):

    ax, ay = sef.accl(x, y)
    vx, vy = sef.vel(x, y, vx, vy, ax, ay, dt)
    x, y = sef.posn(x, y, vx, vy, dt)

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

plt.show()