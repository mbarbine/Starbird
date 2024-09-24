# modules/story.py

import pygame
import logging
import os
import sys
from modules.settings import *

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
    if BACKGROUND_MUSIC and os.path.exists(os.path.join('assets', BACKGROUND_MUSIC)):
        try:
            pygame.mixer.music.load(os.path.join('assets', BACKGROUND_MUSIC))
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # Loop indefinitely
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
        screen.fill(BACKGROUND_COLOR)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + i * line_height))
            screen.blit(text_surface, text_rect)

        # Update the y-offset to scroll the text
        y_offset -= SCROLL_SPEED

        pygame.display.flip()
        clock.tick(FPS)

    # Clear the screen after the intro
    screen.fill(BLACK)
    pygame.display.flip()

    # Stop background music after intro if playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(MUSIC_FADEOUT_TIME)
    logging.info("Star Wars intro completed.")

def read_story_text(filename):
    """
    Reads and parses the story text from a file into a dictionary of levels.

    Args:
        filename (str): The path to the story text file.

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
                    current_level = line
                    story_dict[current_level] = ""
                elif current_level:
                    story_dict[current_level] += line + "\n"
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")
    return story_dict

def display_story(screen, font, story, level_key):
    """
    Displays the story text for a specific level on the screen.

    Args:
        screen (pygame.Surface): The game screen surface.
        font (pygame.font.Font): The font object to render text.
        story (dict): A dictionary with levels as keys and story texts as values.
        level_key (str): The level key to retrieve and display text for.
    """
    text = story.get(level_key, "Story not found for this level.")
    lines = text.split('\n')
    screen.fill(BACKGROUND_COLOR)

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4 + i * FONT_SIZE))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    logging.info(f"Displayed story for {level_key}")

def load_story(filename='assets/story.txt'):
    """
    Loads and returns the story text as a dictionary.

    Args:
        filename (str): The path to the story text file.

    Returns:
        dict: A dictionary with levels as keys and story text as values.
    """
    if not os.path.exists(filename):
        logging.error(f"Story file not found: {filename}")
        return {}

    return read_story_text(filename)
