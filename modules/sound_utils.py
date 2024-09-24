# modules/sound_utils.py

import pygame
import os
import logging
from modules.settings import SOUNDS, SFX_VOLUME, MUSIC_VOLUME

def load_sound(effect_name):
    """Loads a sound from the SOUNDS dictionary."""
    sound_path = SOUNDS.get(effect_name)
    if sound_path and os.path.exists(sound_path):
        try:
            sound = pygame.mixer.Sound(sound_path)
            logging.info(f"Loaded sound: {sound_path}")
            return sound
        except pygame.error as e:
            logging.error(f"Failed to load sound {sound_path}: {e}")
    else:
        logging.error(f"Sound file {sound_path} not found.")
    return None

def play_background_music():
    """Plays background music in a loop."""
    music_path = SOUNDS['BACKGROUND_MUSIC']
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            logging.info(f"Playing background music: {music_path}")
        except pygame.error as e:
            logging.error(f"Failed to play background music {music_path}: {e}")
    else:
        logging.error(f"Background music file {music_path} not found.")

def play_sound_effect(effect_name):
    """Plays a specified sound effect."""
    sound_effect = load_sound(effect_name)
    if sound_effect:
        sound_effect.set_volume(SFX_VOLUME)
        sound_effect.play()

def activate_lightsaber(screen, bird):
    """
    Activates the lightsaber effect.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.
        bird (Bird): The bird object to use for lightsaber position.
    """
    # Draw the lightsaber effect
    pygame.draw.line(screen, settings.GREEN, (bird.rect.x + bird.rect.width, bird.rect.centery),
                     (bird.rect.x + bird.rect.width + settings.LIGHTSABER_LENGTH, bird.rect.centery), 5)
    play_sound_effect('LIGHTSABER')
