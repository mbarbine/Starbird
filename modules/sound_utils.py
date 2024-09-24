# modules/sound_utils.py

import pygame
import os
import logging
from modules.settings import SFX_VOLUME, MUSIC_VOLUME

def load_sound(file_name):
    """Load a sound effect from the assets/sounds folder."""
    full_path = os.path.join('assets', 'sounds', file_name)
    try:
        sound = pygame.mixer.Sound(full_path)
        sound.set_volume(SFX_VOLUME)
        logging.info(f"Loaded sound: {full_path}")
        return sound
    except pygame.error as e:
        logging.error(f"Failed to load sound {file_name}: {e}")
        return None

def play_background_music(file_name):
    """Play background music in a loop."""
    full_path = os.path.join('assets', 'sounds', file_name)
    try:
        if os.path.exists(full_path):
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Play in a loop
            logging.info(f"Playing background music: {full_path}")
        else:
            logging.error(f"Background music file {full_path} not found.")
    except pygame.error as e:
        logging.error(f"Failed to play background music {file_name}: {e}")

def play_lightsaber_sound():
    """Play the lightsaber sound effect."""
    lightsaber_sound = load_sound('lightsaber.wav')
    if lightsaber_sound:
        lightsaber_sound.play()
        logging.info("Lightsaber sound played.")

def play_flap_sound():
    """Play the flap sound effect."""
    flap_sound = load_sound('flap.wav')
    if flap_sound:
        flap_sound.play()
        logging.info("Flap sound played.")

def play_collision_sound():
    """Play the collision sound effect."""
    collision_sound = load_sound('hit.wav')
    if collision_sound:
        collision_sound.play()
        logging.info("Collision sound played.")

def play_shield_sound():
    """Play the shield activation sound effect."""
    shield_sound = load_sound('shield.wav')
    if shield_sound:
        shield_sound.play()
        logging.info("Shield sound played.")

def activate_lightsaber(screen, bird):
    """
    Activates the lightsaber effect.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.
        bird (Bird): The bird object to use for lightsaber position.
    """
    # Draw the lightsaber effect
    pygame.draw.line(screen, settings.GREEN, 
                     (bird.rect.x + bird.rect.width, bird.rect.centery),
                     (bird.rect.x + bird.rect.width + 50, bird.rect.centery), 5)
    play_lightsaber_sound()
