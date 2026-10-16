import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from functions import twoPlanetsFunctions as tpf

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

positions = []

dt = 0.1

for t in np.arange(200):
    a1x, a1y, a2x, a2y = tpf.accl(x1, y1, x2, y2, GM, Gm1,  Gm2)
    v1x, v1y, v2x, v2y = tpf.vel(v1x, v1y, v2x, v2y, a1x, a1y, a2x, a2y, dt)
    x1, y1, x2, y2 = tpf.posn(x1, y1, x2, y2, v1x, v1y, v2x, v2y, dt)
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

# uncomment it if you need the webp
#anim.save("3body.webp", writer=PillowWriter(fps=30), dpi=100)

plt.show()