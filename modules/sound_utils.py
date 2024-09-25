# modules/sound_utils.py

import pygame
import os
import logging
from modules.settings import SOUNDS, SFX_VOLUME, MUSIC_VOLUME, COLORS, LIGHTSABER_LENGTH

# Initialize Pygame mixer
pygame.mixer.init()

def load_sound(effect_name):
    """
    Loads a sound from the SOUNDS dictionary.
    
    Args:
        effect_name (str): The name of the sound effect to load.
    
    Returns:
        pygame.mixer.Sound: The loaded sound object, or None if loading fails.
    """
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
    """
    Plays the background music in a loop.
    Uses the 'BACKGROUND_MUSIC' key from the SOUNDS dictionary.
    """
    music_path = SOUNDS.get('BACKGROUND_MUSIC')
    if music_path and os.path.exists(music_path):
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
    """
    Plays a specified sound effect by name.

    Args:
        effect_name (str): The name of the sound effect to play.
    """
    sound_effect = load_sound(effect_name)
    if sound_effect:
        sound_effect.set_volume(SFX_VOLUME)
        sound_effect.play()
        logging.info(f"Playing sound effect: {effect_name}")

def activate_lightsaber(screen, bird):
    """
    Activates the lightsaber effect visually and plays the sound.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.
        bird (Bird): The bird object to use for lightsaber position.
    """
    # Draw the lightsaber effect
    start_pos = (bird.rect.x + bird.rect.width, bird.rect.centery)
    end_pos = (bird.rect.x + bird.rect.width + LIGHTSABER_LENGTH, bird.rect.centery)
    pygame.draw.line(screen, COLORS['GREEN'], start_pos, end_pos, 5)
    play_sound_effect('LIGHTSABER')
    logging.info("Activated lightsaber effect.")

def stop_background_music():
    """
    Stops the background music playback.
    """
    try:
        pygame.mixer.music.stop()
        logging.info("Background music stopped.")
    except pygame.error as e:
        logging.error(f"Failed to stop background music: {e}")

def adjust_volume(effect_name=None, music_volume=None, sfx_volume=None):
    """
    Adjusts the volume of music and sound effects.

    Args:
        effect_name (str, optional): The name of the sound effect to adjust volume. Defaults to None.
        music_volume (float, optional): Volume level for music [0.0, 1.0]. Defaults to None.
        sfx_volume (float, optional): Volume level for sound effects [0.0, 1.0]. Defaults to None.
    """
    if music_volume is not None:
        pygame.mixer.music.set_volume(music_volume)
        logging.info(f"Music volume set to {music_volume}")

    if sfx_volume is not None and effect_name:
        sound_effect = load_sound(effect_name)
        if sound_effect:
            sound_effect.set_volume(sfx_volume)
            logging.info(f"Volume for {effect_name} set to {sfx_volume}")

def fade_out_music(duration):
    """
    Fades out the background music over the specified duration.

    Args:
        duration (int): Fade-out duration in milliseconds.
    """
    try:
        pygame.mixer.music.fadeout(duration)
        logging.info(f"Background music fading out over {duration}ms.")
    except pygame.error as e:
        logging.error(f"Failed to fade out music: {e}")
