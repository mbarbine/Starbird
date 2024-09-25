# modules/sound_effects.py

import pygame
import os
import logging
import modules.settings as settings
settings.init()


SFX_VOLUME = settings.SFX_VOLUME
COLORS = settings.COLORS
GREEN = COLORS['GREEN']
MUSIC_VOLUME = settings.MUSIC_VOLUME

# Initialize Pygame mixer
pygame.mixer.init()


def load_sound(sound_path):
    """Loads a sound from the given path."""
    full_path = os.path.join('assets', sound_path)
    try:
        sound = pygame.mixer.Sound(full_path)
        logging.info(f"Loaded sound: {full_path}")
        return sound
    except pygame.error as e:
        logging.error(f"Failed to load sound {full_path}: {e}")
        return None  # Return None if loading fails
    

def play_background_music(music_path):
    """Plays background music."""
    full_path = os.path.join('assets', music_path)
    if os.path.exists(full_path):
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            logging.info(f"Playing background music: {full_path}")
        except pygame.error as e:
            logging.error(f"Failed to play background music {full_path}: {e}")
    else:
        logging.error(f"Background music file {full_path} not found.")




def play_lightsaber_sound():
    """Plays the lightsaber sound effect."""
    lightsaber_sound = load_sound('sounds/lightsaber.wav')
    if lightsaber_sound:
        lightsaber_sound.set_volume(SFX_VOLUME)
        lightsaber_sound.play()


def activate_lightsaber(screen, bird):
    """
    Activates the lightsaber effect.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.
        bird (Bird): The bird object to use for lightsaber position.
    """
    # Draw the lightsaber effect
    pygame.draw.line(screen, GREEN, (bird.rect.x + bird.rect.width, bird.rect.centery),
                     (bird.rect.x + bird.rect.width + 50, bird.rect.centery), 5)
    play_lightsaber_sound()
    
