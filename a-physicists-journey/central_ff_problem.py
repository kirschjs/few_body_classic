import time
import numpy as np
import pygame

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 2000
ON_SCREEN_ORIGIN = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))


def model_to_screen(coords):
    return (ON_SCREEN_ORIGIN[0] + coords[0], ON_SCREEN_ORIGIN[1] - coords[1])


CHARCOAL = (54, 69, 79)

t_initial = 0
t_final = 2e3
dt = .3

# model system:
number_of_particles = 10

particle_color = np.tile([204, 17, 0], [number_of_particles, 1])

particle_size = np.tile(6, [number_of_particles, 1])

r0 = np.random.randint(low=20, high=160, size=(number_of_particles, 2))
initial_distances_from_center = [np.sqrt(r[0]**2 + r[1]**2) for r in r0]

v0 = np.random.uniform(low=-0.1, high=.12, size=(number_of_particles, 2))

force_strength = 3
fermi_depth = 0.
fermi_slope = 3.2
fermi_radius = 200


# 1/r potential with centre at the origin => -k*r/r^3 force
# particle masses are identical and set to 1
def gforce(coords, k):

    dist_vecs = [np.sqrt(coord[0]**2 + coord[1]**2) for coord in coords]
    frc = [
        k * np.array(
            [-coords[i][0] / dist_vecs[i]**3, -coords[i][1] / dist_vecs[i]**3])
        for i in range(len(coords))
    ]

    return frc


# potential approximation of spatial confinement to a finite volume
# here: circular disk around the origin with extend r0 and steepness k
def fforce(coords, l, k, r0):

    dist_vecs = [np.sqrt(coord[0]**2 + coord[1]**2) for coord in coords]
    frc = [
        -l / (dist_vecs[i] * k) * np.exp(
            (dist_vecs[i] - r0) / k) / (np.exp(-k * (dist_vecs[i] - r0)) + 1)**
        2 * np.array([coords[i][0], coords[i][1]]) for i in range(len(coords))
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
        v[particle] + (gforce(r2, force_strength)[particle] + fforce(
            r2, fermi_depth, fermi_slope, fermi_radius)[particle]) * dt
        for particle in range(number_of_particles)
    ]
    #print(r2, v)
    #exit()
    # visualize system at t+dt
    screen.fill(CHARCOAL)
    for particle in range(number_of_particles):

        ri2 = np.array(model_to_screen(r2[particle]))

        try:
            pygame.draw.circle(screen, particle_color[particle],
                               ri2.astype(int), particle_size[particle])
        except:
            print(r2, '\n', v0)
            exit()

# Draw by flipping buffer (double-buffering).
    pygame.display.flip()
    t += dt
