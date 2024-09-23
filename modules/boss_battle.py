import pygame
from modules.settings import *
class BossBattle:
    def __init__(self, boss_image_path):
        self.image = pygame.image.load(boss_image_path)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - self.rect.width
        self.rect.y = HEIGHT // 4
        self.health = 100

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True  # Boss defeated
        return False

def boss_fight(bird, boss):
    if bird.colliderect(boss.rect):
        boss.take_damage(10)
