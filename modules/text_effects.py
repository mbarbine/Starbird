# modules/text_effects.py

import pygame
from modules.settings import *

# Define colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


def render_star_wars_text(text, screen, scroll_speed=2):
    """
    Renders the given text in a Star Wars-style scrolling effect.

    Args:
        text (str): The text to render.
        screen (pygame.Surface): The Pygame screen surface to render on.
        scroll_speed (int, optional): The speed of text scrolling. Default is 2.
    """
    font = pygame.font.Font(None, 40)
    lines = text.split('\n')
    y_offset = HEIGHT
    line_height = font.get_linesize()

    running = True
    while running and y_offset > -len(lines) * line_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    running = False

        screen.fill(BLACK)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, YELLOW)
            # Center the text horizontally on the screen
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + i * line_height))
            screen.blit(text_surface, text_rect)

        y_offset -= scroll_speed  # Variable scroll speed for better control
        pygame.display.flip()
        pygame.time.wait(10)  # Adjust value for smoother scrolling

    # Optional: Clear the screen after the intro
    screen.fill(BLACK)
    pygame.display.flip()


def read_story_text(filename, line_number):
    """
    Reads a specific line from the story text file.

    Args:
        filename (str): The path to the story text file.
        line_number (int): The line number to read.

    Returns:
        str: The content of the specified line, or error message if not found.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if 0 <= line_number < len(lines):
                return lines[line_number].strip()
            else:
                return "Line not found."
    except FileNotFoundError:
        return f"File {filename} not found."
    except Exception as e:
        return f"Error reading file: {e}"


def render_story_text(screen, text, display_time=3000):
    """
    Renders the story text on the screen for a specified duration.

    Args:
        screen (pygame.Surface): The Pygame screen surface to render on.
        text (str): The text to render.
        display_time (int, optional): Time in milliseconds to display the text. Default is 3000ms.
    """
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center text on the screen
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(display_time)  # Wait for specified display time


def draw_text(text, font, color, x, y, screen, center=False):
    """
    Renders text on the screen with optional centering.

    Args:
        text (str): The text to render.
        font (pygame.font.Font): The font object to render the text with.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        screen (pygame.Surface): The screen surface to render the text on.
        center (bool, optional): Whether to center the text horizontally. Default is False.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
