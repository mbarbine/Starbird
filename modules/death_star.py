import pygame
from settings import *
class DeathStar:
    def __init__(self):
        self.image = pygame.image.load('assets/death_star.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.rect.width
        self.rect.y = HEIGHT // 4
        self.health = 100

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        # Quantum-based health reduction
        quantum_reduction = random.uniform(0.8, 1.2)
        self.health -= int(amount * quantum_reduction)
        if self.health <= 0:
            return True  # Destroyed
        return False

def death_star_battle(screen, bird):
    death_star = DeathStar()
    while death_star.health > 0:
        screen.fill(BLACK)
        death_star.draw(screen)
        pygame.display.flip()
        
        # Handle player actions and damage Death Star
        if bird.colliderect(death_star.rect):
            if death_star.take_damage(10):  # Example damage value
                break  # Death Star destroyed
        
        pygame.time.wait(50)




#from death_star import death_star_battle

#def trigger_death_star_battle():
#    if current_level == 3:  # Example condition
#        death_star_battle(screen, bird)
#
## Trigger Death Star battle at the end of certain levels
#trigger_death_star_battle()
#
