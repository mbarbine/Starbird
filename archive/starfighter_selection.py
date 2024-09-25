import pygame
from modules.settings import *
class Starfighter:
    def __init__(self, image_path, ability):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.ability = ability

    def draw(self, screen, position):
        screen.blit(self.image, position)

def select_starfighter():
    x_wing = Starfighter('assets/x_wing.png', 'Laser')
    tie_fighter = Starfighter('assets/tie_fighter.png', 'Speed')
    millennium_falcon = Starfighter('assets/millennium_falcon.png', 'Shield')

    starfighters = [x_wing, tie_fighter, millennium_falcon]
    selected_starfighter = None

    while selected_starfighter is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_starfighter = x_wing
                elif event.key == pygame.K_2:
                    selected_starfighter = tie_fighter
                elif event.key == pygame.K_3:
                    selected_starfighter = millennium_falcon

        # Draw selection screen
        screen.fill(BLACK)
        for i, starfighter in enumerate(starfighters):
            starfighter.draw(screen, (100 * (i + 1), HEIGHT // 2))
        pygame.display.flip()

    return selected_starfighter



#from starfighter_selection import select_starfighter

# At the start of the game
#selected_starfighter = select_starfighter()

# Use selected starfighter's abilities during gameplay
#if selected_starfighter.ability == 'Laser':
#    activate_force_lightning(obstacles)
#elif selected_starfighter.ability == 'Speed':
#    bird_velocity += 2  # Example speed boost
#elif selected_starfighter.ability == 'Shield':
#    activate_force_shield(bird)


