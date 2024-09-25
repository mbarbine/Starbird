# modules/story.py

import os
import pygame
import logging
import sys
from modules.settings import (
    STORY_MD_PATH,  # Path to story.md
    COLORS,
    WIDTH,
    HEIGHT,
    FONT_SIZE,
    SCROLL_SPEED,
    FPS,
    MUSIC_VOLUME,
    MUSIC_FADEOUT_TIME
)

def star_wars_intro(text, screen):
    """
    Displays a scrolling Star Wars-style intro text with customizable settings.

    Args:
        text (str): The intro text to display.
        screen (pygame.Surface): The game screen surface.
    """
    # Set up font and colors
    try:
        font = pygame.font.Font(None, FONT_SIZE)
    except pygame.error as e:
        logging.error(f"Font loading error: {e}")
        font = pygame.font.SysFont(None, FONT_SIZE)

    # Split text into lines and calculate total height
    lines = text.split('\n')
    line_height = font.get_linesize()
    text_height = len(lines) * line_height
    y_offset = HEIGHT

    # Initialize background music if specified in settings
    background_music_path = os.path.join('assets', 'sounds', 'background_music.mp3')
    if os.path.exists(background_music_path):
        try:
            pygame.mixer.music.load(background_music_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            logging.info("Background music started.")
        except pygame.error as e:
            logging.error(f"Error loading background music: {e}")

    # Main loop for scrolling text
    running = True
    clock = pygame.time.Clock()
    while running and y_offset > -text_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    running = False  # Exit loop on space or enter key

        # Clear screen and draw the text
        screen.fill(COLORS['BACKGROUND'])  # Use the BACKGROUND color from the COLORS dictionary
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, COLORS['TEXT'])  # Use TEXT color from COLORS
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + i * line_height))
            screen.blit(text_surface, text_rect)

        # Update the y-offset to scroll the text
        y_offset -= SCROLL_SPEED

        pygame.display.flip()
        clock.tick(FPS)

    # Clear the screen after the intro
    screen.fill(COLORS['BLACK'])  # Use BLACK from COLORS
    pygame.display.flip()

    # Stop background music after intro if playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(MUSIC_FADEOUT_TIME)
    logging.info("Star Wars intro completed.")

def read_story_text(filename):
    """
    Reads and parses the story text from a markdown file into a dictionary of levels.

    Args:
        filename (str): The path to the story markdown file.

    Returns:
        dict: A dictionary with levels as keys and story text as values.
    """
    story_dict = {}
    current_level = ""
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("# Level"):
                    # Extract level number and name
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        # Example: "# Level1 (Level Name)"
                        level_info = parts[2]
                        if '(' in level_info and ')' in level_info:
                            level_number, level_name = level_info.split('(', 1)
                            level_number = level_number.strip()
                            level_name = level_name.strip(' )')
                            current_level = f"# Level{level_number} ({level_name})"
                            story_dict[current_level] = ""
                elif current_level:
                    story_dict[current_level] += line + "\n"
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")
    return story_dict

def get_story_text(level_number):
    """
    Retrieves the story text for a given level number from the story markdown file.

    Args:
        level_number (int): The level number.

    Returns:
        str: The story text for the level.
    """
    story_dict = read_story_text(STORY_MD_PATH)
    level_key_prefix = f"# Level{level_number}"
    # Find the key that starts with level_key_prefix
    for key in story_dict:
        if key.startswith(level_key_prefix):
            return story_dict[key]
    return "No story available for this level."
