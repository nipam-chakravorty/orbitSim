# This model is to produce an 3D arrangement of the sunEarth model
# To model the magnetic field of the star a current carrying loop
# the star in this case is to be a static object without precession or field flip
# the magentic field is to be modelled as uniform without any fluctuation

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import cm, colors
from functions import sunEarthFunctions as sef

class Star:
    def __init__(self, mass, x, y, z):
        self.mass = mass
        # position of the star
        self.x = x
        self.y = y
        self.z = z
    def GM (self):
        _GM = 4 * np.pi * np.pi / self.mass
        return _GM
    def dm (self):
        # dipole moment
        _dm = 1
        return _dm

class Planet:
    def __init__(self, x, y, z, vx, vy):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        # movement of the planet is restricted to the xy-plane

    def dm(self):
        # dipole moment
        _dm = 0.01
        return 0.01

def magField(x, y, z, dipole_moment):
    mu_0 = 1
    dipole_moment = 1

    C = (mu_0 * dipole_moment) / (4 * np.pi)

    r = np.sqrt(x*x + y*y + z*z)
    r5 = r ** 5

    B_x = C * 3 * x * z / r5
    B_y = C * 3 * y * z / r5
    B_z = C * (2*z*z - x*x - y*y) / r5

    return B_x, B_y, B_z

sun = Star(1, 0, 0, 0)
earth = Planet(1, 0 , 0, 0, np.sqrt(sun.GM()/1))

positions = [(earth.x,earth.y)]

dt = 0.01

for _ in range(200):
    earth.x, earth.y, earth.vx, earth.vy = sef.RK4(earth.x, earth.y, earth.vx, earth.vy, dt)
    positions.append([earth.x, earth.y])

positions = np.array(positions)

# ---------- plot block : orbit + Sun & Earth dipole fields (animated) ----------

# 1) Build the field grid (same as before)
n = 6                                   # even n avoids sampling the origin (r = 0)
axis = np.linspace(-2, 2, n)
X, Y, Z = np.meshgrid(axis, axis, axis)

# 2) Total field = Sun's dipole + Earth's dipole (superposition principle)
def total_field(px, py):
    """Total B at every grid point when Earth is at (px, py, earth.z)."""
    # Sun's dipole: centred on the origin
    Bx_s, By_s, Bz_s = magField(X, Y, Z, sun.dm())
    Bx_s, By_s, Bz_s = sun.dm() * Bx_s, sun.dm() * By_s, sun.dm() * Bz_s

    # Earth's dipole: same formula, but measured from Earth's position
    with np.errstate(divide="ignore", invalid="ignore"):
        Bx_e, By_e, Bz_e = magField(X - px, Y - py, Z - earth.z, earth.dm())
    Bx_e, By_e, Bz_e = (earth.dm() * np.nan_to_num(Bx_e),
                        earth.dm() * np.nan_to_num(By_e),
                        earth.dm() * np.nan_to_num(Bz_e))

    Bx, By, Bz = Bx_s + Bx_e, By_s + By_e, Bz_s + Bz_e
    return Bx, By, Bz, np.sqrt(Bx**2 + By**2 + Bz**2)

# 3) Interaction energy of Earth's dipole (along +z) in the Sun's field: U = -m . B_sun
def interaction_energy(px, py):
    _, _, Bz_sun = magField(px, py, earth.z, sun.dm())
    return -earth.dm() * sun.dm() * Bz_sun

# 4) Fixed colour scale over the WHOLE orbit, so colours are comparable between frames
all_mags = np.concatenate([total_field(px, py)[3].ravel() for px, py in positions])
all_mags = all_mags[all_mags > 0]
norm = colors.LogNorm(vmin=all_mags.min(), vmax=all_mags.max())

# 5) Set up the 3D figure
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(projection="3d")

def draw_field(px, py):
    Bx, By, Bz, B_mag = total_field(px, py)
    rgba = cm.viridis(norm(np.clip(B_mag.ravel(), norm.vmin, norm.vmax)))
    rgba[:, 3] = 0.3                         # alpha of the arrows
    # 3D quiver draws 3 segments per arrow (shaft + 2 head strokes)
    rgba = np.concatenate((rgba, np.repeat(rgba, 2, axis=0)))
    return ax.quiver(X, Y, Z, Bx, By, Bz, length=0.5, normalize=True, colors=rgba)

quiv = [draw_field(*positions[0])]      # list so update() can replace it

ax.scatter(sun.x, sun.y, sun.z, color="orange", s=150, label="Star")

ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-3, 3)
ax.set_box_aspect((1, 1, 1))
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title("Star + planet dipole fields (superposition)")

sm = cm.ScalarMappable(norm=norm, cmap="viridis")
fig.colorbar(sm, ax=ax, shrink=0.6, label="|B_total| (log scale)")

# 6) Animated artists
planet, = ax.plot([], [], [], "bo", markersize=8, label="Planet")
trail,  = ax.plot([], [], [], "b-", alpha=0.5)
energy_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)
ax.legend()

# 7) Update function: called once per frame
def update(frame):
    px, py = positions[frame]
    planet.set_data([px], [py])
    planet.set_3d_properties([0])

    trail.set_data(positions[:frame+1, 0], positions[:frame+1, 1])
    trail.set_3d_properties(np.zeros(frame + 1))

    quiv[0].remove()                    # quiver can't be edited, so redraw it
    quiv[0] = draw_field(px, py)

    energy_text.set_text(f"U = -m·B_sun = {interaction_energy(px, py):.2e}")
    return planet, trail, quiv[0], energy_text

anim = FuncAnimation(fig, update, frames=len(positions), interval=30, blit=False)
#anim.save("orbit_dipole.gif", writer=PillowWriter(fps=30))   # uncomment to save
plt.show()