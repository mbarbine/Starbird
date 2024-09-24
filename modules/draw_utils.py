# modules/draw_utils.py
import pygame
import logging
from modules.bird import Bird
from modules.pipe import Pipe
import modules.settings as settings

def draw_game_elements(screen, bird, obstacles, quantum_elements):
    """Draws all game elements on the screen."""
    bird.draw(screen)
    draw_obstacles(screen, obstacles)
    draw_quantum_elements(screen, quantum_elements)

def draw_obstacles(screen, obstacles):
    """Draws all obstacles on the screen."""
    for obstacle in obstacles:
        if hasattr(obstacle, 'draw'):
            obstacle.draw(screen)
        else:
            logging.error(f"Obstacle {obstacle} does not have a 'draw' method.")

def draw_quantum_elements(screen, quantum_elements):
    """Draws all quantum elements on the screen."""
    for element in quantum_elements:
        if hasattr(element, 'draw'):
            element.draw(screen)
        else:
            logging.error(f"Quantum element {element} does not have a 'draw' method.")

def draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level):
    """Draws the Heads-Up Display (HUD) on the screen."""
    draw_text(f"Score: {score}", font, settings.BLUE, 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, settings.RED, 10, 50, screen)
    draw_text(f"Level: {current_level}", font, settings.GREEN, 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, settings.YELLOW, 10, 130, screen)
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, settings.CYAN, 10, 170, screen)
    draw_text(f"Velocity: {bird.velocity:.2f}", font, settings.WHITE, 10, 210, screen)
    if pygame.time.get_ticks() - control_display_timer < settings.CONTROL_DISPLAY_TIME:
        draw_text("Space: Flap, S: Shield, L: Lightsaber, P: Pause", font, settings.WHITE, 10, settings.HEIGHT - 50, screen)
