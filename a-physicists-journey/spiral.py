from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')

z = np.linspace(0, 3, 1500)
x = -np.exp(-0.5 * z**2) * np.sin(20 * z)
y = -np.exp(-0.5 * z**2) * np.cos(20 * z)

ax.plot3D(x, y, -z, 'maroon')

z = np.linspace(2, 6, 1500)
x = -np.exp(-0.025 * z**0.5) * np.sin(20 * z)
y = -np.exp(-0.025 * z**0.5) * np.cos(20 * z)

ax.plot3D(x, y, -z, 'blue')

ax.axis('off')
ax.set_facecolor('white')
ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.w_zaxis.line.set_visible(False)

ax.set_title('')
fig.savefig("spiral.png")