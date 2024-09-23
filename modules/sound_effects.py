import pygame
from modules.settings import *

def play_lightsaber_sound():
    pygame.mixer.init()
    lightsaber_sound = pygame.mixer.Sound('assets/lightsaber.wav')
    lightsaber_sound.play()
from sound_effects import play_lightsaber_sound

def activate_lightsaber():
    # Lightsaber effect
    pygame.draw.line(screen, GREEN, (bird.x, bird.y), (bird.x + 50, bird.y), 5)
    play_lightsaber_sound()

# Call activate_lightsaber at random moments or specific events
