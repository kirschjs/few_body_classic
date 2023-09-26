import time
import numpy as np
import matplotlib.pyplot as plt
import more_itertools
import pygame

pygame.init()
infos = pygame.display.Info()
screen_size = (infos.current_w, infos.current_h)

SCREEN_WIDTH = screen_size[0]
SCREEN_HEIGHT = screen_size[1]
ON_SCREEN_ORIGIN = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))


def model_to_screen(coords):
    return (ON_SCREEN_ORIGIN[0] + coords[0], ON_SCREEN_ORIGIN[1] + coords[1])


CHARCOAL = (54, 69, 79)

t_initial = 0
t_final = 1e3
dt = 1.0

# model system:
number_of_particles = 2

particle_color = np.tile([204, 17, 0], [number_of_particles, 1])

particle_size = list(
    more_itertools.collapse(np.tile(6, [number_of_particles, 1])))

r0 = np.random.randint(low=-20, high=60, size=(number_of_particles, 2))
r0 = np.tile([100, 100], (2, 1))

initial_distances_from_center = [np.sqrt(r[0]**2 + r[1]**2) for r in r0]

v0 = np.random.uniform(low=-0.5, high=0.5, size=(number_of_particles, 2))

force_strength = 323
center_color = [250, 255, 250]
center_size = 7
R_cut = center_size
fermi_depth = 0.
fermi_slope = 3.2
fermi_radius = 200


# 1/r potential with centre at pos c => -k*(r-c)/(r-c)^3 force
# particle masses are identical and set to 1
# if the particles' distance to a center is less than the center's plus the particle's
# radius, the particle experiences a repulsion
def gforce(coords, k, cntr=[0, 0]):

    dist_vecs = [
        np.sqrt((coord[0] - cntr[0])**2 + (coord[1] - cntr[1])**2)
        for coord in coords
    ]

    frc = []
    for i in range(len(coords)):

        if dist_vecs[i] == 0.0:
            frc.append(np.array([0, 0]))
        elif 0 < dist_vecs[i] < (R_cut + particle_size[i]):
            frc.append(
                np.abs(0.0001 * k) * np.array([
                    np.abs(coords[i][0] - cntr[0]) / dist_vecs[i]**1,
                    np.abs(coords[i][1] - cntr[1]) / dist_vecs[i]**1
                ]))
        elif dist_vecs[i] > R_cut + particle_size[i]:
            frc.append(k * np.array([
                -(coords[i][0] - cntr[0]) / dist_vecs[i]**3,
                -(coords[i][1] - cntr[1]) / dist_vecs[i]**3
            ]))

    return frc


# potential approximation of spatial confinement to a finite volume
# here: circular disk around the origin with extend r0 and steepness k
def fforce(coords, l, k, r0):

    dist_vecs = [np.sqrt(coord[0]**2 + coord[1]**2) for coord in coords]
    frc = [
        -l / (dist_vecs[i] * k) * np.exp((dist_vecs[i] - r0) / k) /
        (np.exp(-k * (dist_vecs[i] - r0)) + 1)**2 *
        np.array([coords[i][0], coords[i][1]]) for i in range(len(coords))
    ]
    #if abs(frc[0][0] > 1):
    #    print(frc)
    #    time.sleep(5)
    return frc


pygame.init()
# Open a single window with set dimensions.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

t = t_initial
r1 = r0

# define a set of force centers; cf. locations of assumed infinitely
# heavy nulcei/suns/etc.
# place N nuclei symmetrically on a circle of radius R around the origin
nbr_centers = 5
R_centers = 100
force_centers = [[
    R_centers * np.cos(nc * 2 * np.pi / nbr_centers),
    R_centers * np.sin(nc * 2 * np.pi / nbr_centers)
] for nc in range(nbr_centers)]

phase_space = []

while t < t_final:

    v = v0
    # calculate new position vector: r(t+dt) = r(t) + v(t)*dt
    r2 = [
        np.array([
            r1[particle][0] + v0[particle][0] * dt,
            r1[particle][1] + v0[particle][1] * dt
        ]) for particle in range(number_of_particles)
    ]

    r1 = r2

    v0 = [
        v[particle] + (
            sum(
                np.array([
                    gforce(r2, force_strength, cntr=cc)[particle]
                    for cc in force_centers
                ]))
            #+ fforce(r2, fermi_depth, fermi_slope, fermi_radius)[particle]
        ) * dt for particle in range(number_of_particles)
    ]
    phase_space.append([r2, v])
    screen.fill(CHARCOAL)
    # draw the locations of the ``nuclei'' (force centers)
    for cc in force_centers:
        ri = np.array(model_to_screen(cc))
        pygame.draw.circle(screen, center_color, ri.astype(int), center_size)

    # visualize system at t+dt
    for particle in range(number_of_particles):

        ri2 = np.array(model_to_screen(r2[particle]))
        try:
            pygame.draw.circle(screen, particle_color[particle],
                               ri2.astype(int), particle_size[particle])
        except:
            print('pygame run-time error:\nr=', r2, ri2, '\nv=', v0)
            exit()

# Draw by flipping buffer (double-buffering).
    pygame.display.flip()
    t += dt

yy = np.array(phase_space)[:, 0][:, 0][:, 0]
xx = range(len(yy))
fig, ax = plt.subplots()

#ax.set_xlim(0, rmax)
#ax.set_ylim(-20, 20)

ax.plot(xx, yy, label=r'')

ax.set(xlabel=r'distance from the center $|\mathbf{r}|$ [fm]',
       ylabel=r'potential $V(|\mathbf{r}|)$',
       title='About as simple as it gets, folks')
ax.grid()

plt.legend(loc='best', numpoints=1)

fig.savefig("classical_orbits.png")
#plt.show()