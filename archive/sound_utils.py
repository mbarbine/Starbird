# modules/sound_utils.py

import pygame
import os
import logging
from modules.settings import SOUNDS, SFX_VOLUME, MUSIC_VOLUME, COLORS, LIGHTSABER_LENGTH
# from modules.settings import SOUNDS  
# from modules.settings import SFX_VOLUME
# from modules.settings import MUSIC_VOLUME
from modules.settings import COLORS
from modules.settings import LIGHTSABER_LENGTH
class SoundManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SoundManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._init_mixer()

    def _init_mixer(self):
        try:
            pygame.mixer.init()
            logging.info("Pygame mixer initialized.")
        except pygame.error as e:
            logging.error(f"Failed to initialize Pygame mixer: {e}")



    def play_background_music(self):
        music_path = SOUNDS.get('BACKGROUND_MUSIC')
        if music_path:
            full_path = os.path.join('assets', 'sounds', music_path)
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
        else:
            logging.error("BACKGROUND_MUSIC not defined in SOUNDS.")

    def stop_background_music(self):
        try:
            pygame.mixer.music.stop()
            logging.info("Background music stopped.")
        except pygame.error as e:
            logging.error(f"Failed to stop background music: {e}")

    def adjust_volume(self, effect_name=None, music_volume=None, sfx_volume=None):
        if music_volume is not None:
            pygame.mixer.music.set_volume(music_volume)
            logging.info(f"Music volume set to {music_volume}")

        if sfx_volume is not None and effect_name:
            sound_effect = self.load_sound(effect_name)
            if sound_effect:
                sound_effect.set_volume(sfx_volume)
                logging.info(f"Volume for {effect_name} set to {sfx_volume}")

    def fade_out_music(self, duration):
        try:
            pygame.mixer.music.fadeout(duration)
            logging.info(f"Background music fading out over {duration}ms.")
        except pygame.error as e:
            logging.error(f"Failed to fade out music: {e}")

    def activate_lightsaber(self, screen, bird):
        start_pos = (bird.rect.x + bird.rect.width, bird.rect.centery)
        end_pos = (bird.rect.x + bird.rect.width + LIGHTSABER_LENGTH, bird.rect.centery)
        pygame.draw.line(screen, COLORS['GREEN'], start_pos, end_pos, 5)
        self.play_sound_effect('LIGHTSABER')
        logging.info("Activated lightsaber effect.")
