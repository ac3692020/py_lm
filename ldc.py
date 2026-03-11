import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Parameters
# -----------------------
nx = 41
ny = 41
nt = 500
nit = 50
c = 1
dx = 1 / (nx - 1)
dy = 1 / (ny - 1)
rho = 1
nu = 0.1
dt = 0.001

# -----------------------
# Field Variables
# -----------------------
u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))

# -----------------------
# Build RHS of pressure Poisson equation
# -----------------------
def build_up_b(b, rho, dt, u, v, dx, dy):
    b[1:-1, 1:-1] = (rho * (
        1 / dt * ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) +
                  (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) -
        ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 -
        2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) *
             (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
        ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2))
    return b

# -----------------------
# Pressure Poisson Solver
# -----------------------
def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p)
    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 +
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)) -
                         dx**2 * dy**2 /
                         (2 * (dx**2 + dy**2)) * b[1:-1, 1:-1])

        # Pressure BCs
        p[:, -1] = p[:, -2]
        p[:, 0] = p[:, 1]
        p[0, :] = p[1, :]
        p[-1, :] = 0

    return p

# -----------------------
# Time Marching
# -----------------------
for n in range(nt):
    un = u.copy()
    vn = v.copy()

    b = build_up_b(b, rho, dt, u, v, dx, dy)
    p = pressure_poisson(p, dx, dy, b)

    u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                     un[1:-1, 1:-1] * dt / dx *
                     (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                     vn[1:-1, 1:-1] * dt / dy *
                     (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                     dt / (2 * rho * dx) *
                     (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                     nu * (dt / dx**2 *
                     (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                     dt / dy**2 *
                     (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

    v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                     un[1:-1, 1:-1] * dt / dx *
                     (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                     vn[1:-1, 1:-1] * dt / dy *
                     (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                     dt / (2 * rho * dy) *
                     (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                     nu * (dt / dx**2 *
                     (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                     dt / dy**2 *
                     (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

    # Velocity BCs
    u[0, :] = 0
    u[:, 0] = 0
    u[:, -1] = 0
    u[-1, :] = 1      # moving lid

    v[0, :] = 0
    v[-1, :] = 0
    v[:, 0] = 0
    v[:, -1] = 0

# -----------------------
# Plot Results
# -----------------------
X, Y = np.meshgrid(np.linspace(0,1,nx), np.linspace(0,1,ny))

plt.figure(figsize=(8,6))
plt.contourf(X, Y, p, alpha=0.5, cmap='jet')
plt.colorbar()
plt.contour(X, Y, p, cmap='jet')
plt.quiver(X[::2,::2], Y[::2,::2],
           u[::2,::2], v[::2,::2])
plt.title("Lid Driven Cavity Flow")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
