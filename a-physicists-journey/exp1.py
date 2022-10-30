import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ON_SCREEN_ORIGIN = (40, SCREEN_HEIGHT - 40)

CHARCOAL = (54, 69, 79)
CANNON_RED = (204, 17, 0)

CANNONBALL_RADIUS = 5

def model_to_screen(coords):
    return (ON_SCREEN_ORIGIN[0] + coords[0], ON_SCREEN_ORIGIN[1] - coords[1])

# Model:
cannonballs = [(50, 100), (120, 170)]

pygame.init()

# Open a single window with set dimensions.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop.
while True:

    # Rendering
    screen.fill(CHARCOAL)

    # Draw all cannonballs: 
    for cb in cannonballs:
        coords = model_to_screen(cb)
        pygame.draw.circle(screen, CANNON_RED, coords, CANNONBALL_RADIUS)

    # Draw by flipping buffer (double-buffering).
    pygame.display.flip()
