import time
import numpy as np
import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
ON_SCREEN_ORIGIN = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))


def model_to_screen(coords):
    return (ON_SCREEN_ORIGIN[0] + coords[0], ON_SCREEN_ORIGIN[1] - coords[1])


CHARCOAL = (54, 69, 79)

t_initial = 0
t_final = 2e3
dt = .3

# model system:
number_of_particles = 12

particle_color = np.tile([204, 17, 0], [number_of_particles, 1])

particle_size = np.tile(6, [number_of_particles, 1])

r0 = np.random.randint(low=0, high=60, size=(number_of_particles, 2))
initial_distances_from_center = [np.sqrt(r[0]**2 + r[1]**2) for r in r0]

v0 = np.random.uniform(low=0.1, high=.12, size=(number_of_particles, 2))

force_strength = 3
fermi_depth = -100
fermi_slope = 1.2
fermi_radius = 150


# 1/r potential with centre at the origin
def gforce(coords, lec):
    frc = [
        lec * np.array([
            -coord[0] / ((coord[0]**2 + coord[1]**2))**(1.5), -coord[1] /
            (coord[0]**2 + coord[1]**2)**(1.5)
        ]) for coord in coords
    ]
    #print(frc)
    return frc


def fforce(coords, l, k, r0):
    frc = [
        l * k * np.exp(-k * (np.sqrt(coord[0]**2 + coord[1]**2) - r0)) /
        (np.sqrt(coord[0]**2 + coord[1]**2) *
         (np.exp(-k * (np.sqrt(coord[0]**2 + coord[1]**2) - r0)) + 1)**2) *
        np.array([coord[0], coord[1]]) for coord in coords
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
            print(r2, v0)
            exit()

# Draw by flipping buffer (double-buffering).
    pygame.display.flip()
    t += dt