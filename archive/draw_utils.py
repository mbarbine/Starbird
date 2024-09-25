# modules/draw_utils.py

import pygame
import logging
import modules.settings as settings

# Initialize pygame
pygame.init()

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
            logging.error(f"Obstacle {type(obstacle).__name__} does not have a 'draw' method.")

def draw_quantum_elements(screen, quantum_elements):
    """Draws all quantum elements on the screen."""
    for element in quantum_elements:
        if hasattr(element, 'draw'):
            element.draw(screen)
        else:
            logging.error(f"Quantum element {type(element).__name__} does not have a 'draw' method.")

def draw_text(text, font, color, x, y, screen):
    """Draws text on the screen."""
    try:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    except Exception as e:
        logging.error(f"Error drawing text '{text}' at ({x}, {y}): {e}")

def draw_hud(screen, font, score, high_scores, bird, control_display_timer, current_level):
    """Draws the Heads-Up Display (HUD) on the screen."""
    # Using settings.COLORS to access the color values
    draw_text(f"Score: {score}", font, settings.COLORS['BLUE'], 10, 10, screen)
    draw_text(f"High Score: {high_scores['top_score']} by {high_scores['player']}", font, settings.COLORS['RED'], 10, 50, screen)
    draw_text(f"Level: {current_level}", font, settings.COLORS['GREEN'], 10, 90, screen)
    draw_text(f"Lives: {bird.lives}", font, settings.COLORS['YELLOW'], 10, 130, screen)
    
    active_ability = bird.get_current_ability()
    if active_ability:
        draw_text(f"Ability: {active_ability}", font, settings.COLORS['CYAN'], 10, 170, screen)
    
    draw_text(f"Velocity: {bird.velocity:.2f}", font, settings.COLORS['WHITE'], 10, 210, screen)
    
    if pygame.time.get_ticks() - control_display_timer < settings.HUD_SETTINGS['control_display_time']:
        draw_text("Space: Flap, S: Shield, L: Lightsaber, P: Pause", font, settings.COLORS['WHITE'], 10, settings.HEIGHT - 50, screen)
