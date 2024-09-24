# modules/hud.py

import pygame
import logging
from modules.settings import TEXT_COLOR, WIDTH, HEIGHT, CONTROL_DISPLAY_TIME, CONTROL_SETTINGS, FONT_SIZE

def draw_text(text, font, color, x, y, screen):
    """
    Draws text on the screen.

    Args:
        text (str): The text to display.
        font (pygame.font.Font): The font to use for rendering.
        color (tuple): The color of the text.
        x (int): The x-coordinate of the text's position.
        y (int): The y-coordinate of the text's position.
        screen (pygame.Surface): The surface to draw on.
    """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level):
    """
    Draws the Heads-Up Display (HUD) on the screen.

    Args:
        screen (pygame.Surface): The game screen surface.
        font (pygame.font.Font): The font to use for rendering text.
        score (int): The current score.
        high_scores (dict): A dictionary with high score information.
        bird (Bird): The bird object containing current status.
        control_display_timer (int): The timer for displaying controls.
        current_level (int): The current level in the game.
    """
    # Draw score and high score
    draw_text(f"Score: {score}", font, TEXT_COLOR, 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, TEXT_COLOR, 10, 50, screen)
    draw_text(f"Level: {current_level}", font, TEXT_COLOR, 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, TEXT_COLOR, 10, 130, screen)

    # Draw bird's active ability
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, TEXT_COLOR, 10, 170, screen)
    
    # Display current velocity for debugging (optional)
    draw_text(f"Velocity: {bird.velocity:.2f}", font, TEXT_COLOR, 10, 210, screen)

    # Display control instructions for a limited time
    if pygame.time.get_ticks() - control_display_timer < CONTROL_DISPLAY_TIME:
        draw_text("Space: Flap, S: Shield, L: Lightsaber, P: Pause", font, TEXT_COLOR, 10, HEIGHT - 50, screen)
        logging.info("Displaying control instructions.")

def load_game_font():
    """
    Loads the game font.

    Returns:
        pygame.font.Font: The loaded font object.
    """
    try:
        font = pygame.font.Font(None, FONT_SIZE)
        logging.info("Game font loaded successfully.")
        return font
    except pygame.error as e:
        logging.error(f"Error loading font: {e}")
        return pygame.font.SysFont(None, FONT_SIZE)
