import pygame
import os
from settings import *

def render_star_wars_text(text, screen):
    """
    Renders the given text in a Star Wars-style scrolling effect.

    Args:
        text (str): The text to render.
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
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    running = False

        screen.fill(BLACK)
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, YELLOW)
            screen.blit(text_surface, (WIDTH // 4, y_offset + i * line_height))

        y_offset -= 4  # Increase this value for faster scrolling
        pygame.display.flip()
        pygame.time.wait(10)  # Decrease this value for smoother scrolling

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
        str: The content of the specified line.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if line_number < len(lines):
                return lines[line_number].strip()
            else:
                return "Line not found."
    except FileNotFoundError:
        return f"File {filename} not found."
    except Exception as e:
        return f"Error reading file: {e}"

def render_story_text(screen, text):
    """
    Renders the story text on the screen.

    Args:
        screen (pygame.Surface): The Pygame screen surface to render on.
        text (str): The text to render.
    """
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def draw_text(text, font, color, x, y, screen):
    """
    Renders text on the screen.

    Args:
        text (str): The text to render.
        font (pygame.font.Font): The font object to render the text with.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text.
        y (int): The y-coordinate of the text.
        screen (pygame.Surface): The screen surface to render the text on.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
