# modules/story.py

import pygame
import logging
from modules.settings import WIDTH, HEIGHT, BLACK, YELLOW

def star_wars_intro(text, screen):
    """
    Displays the Star Wars-style scrolling intro text.

    Args:
        text (str): The intro text to render.
        screen (pygame.Surface): The Pygame screen surface to render on.
    """
    font = pygame.font.Font(None, 40)
    lines = text.split('\n')
    y_offset = HEIGHT
    line_height = font.get_linesize()

    running = True
    while running and y_offset > -len(lines) * line_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    running = False

        screen.fill(BLACK)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, YELLOW)
            screen.blit(text_surface, (WIDTH // 4, y_offset + i * line_height))

        y_offset -= 4
        pygame.display.flip()
        pygame.time.wait(10)

    # Clear the screen after the intro
    screen.fill(BLACK)
    pygame.display.flip()

def read_story_text(filename):
    """
    Reads the story text from the file and parses it into a dictionary of levels.

    Args:
        filename (str): The path to the story text file.

    Returns:
        dict: A dictionary where each key is a level and the value is the story text for that level.
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
        logging.error(f"Error reading file: {e}")
    return story_dict
