# modules/screen_utils.py

import pygame
import sys
import logging
import modules.settings as settings
from modules.text_effects import draw_text


def init_game_window():
    """Initializes the game window."""
    try:
        if settings.FULLSCREEN:
            screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        logging.info("Game window initialized successfully.")
    except pygame.error as e:
        logging.error(f"Error initializing game window: {e}")
        screen = pygame.display.set_mode((800, 600))  # Fallback resolution
    pygame.display.set_caption(settings.WINDOW_TITLE)
    return screen


def start_screen(screen, font):
    """Displays the Start Screen."""
    screen.fill(settings.START_SCREEN_COLOR)
    title_text = font.render("Starbird", True, settings.BLUE)
    instruction_text = font.render("Press any key to start", True, settings.WHITE)

    screen.blit(title_text, (settings.WIDTH // 2 - title_text.get_width() // 2, settings.HEIGHT // 3))
    screen.blit(instruction_text, (settings.WIDTH // 2 - instruction_text.get_width() // 2, settings.HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event detected on Start Screen.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Start the game


def game_over_screen(screen, font, score, high_scores):
    """Displays the Game Over screen."""
    screen.fill(settings.GAME_OVER_COLOR)
    game_over_text = font.render("Game Over", True, settings.RED)
    score_text = font.render(f"Your Score: {score}", True, settings.WHITE)
    high_score_text = font.render(f"High Score: {high_scores['top_score']} by {high_scores['player']}", True, settings.WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, settings.WHITE)

    screen.blit(game_over_text, (settings.WIDTH // 2 - game_over_text.get_width() // 2, settings.HEIGHT // 4))
    screen.blit(score_text, (settings.WIDTH // 2 - score_text.get_width() // 2, settings.HEIGHT // 2 - 50))
    screen.blit(high_score_text, (settings.WIDTH // 2 - high_score_text.get_width() // 2, settings.HEIGHT // 2))
    screen.blit(retry_text, (settings.WIDTH // 2 - retry_text.get_width() // 2, settings.HEIGHT // 2 + 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event detected on Game Over Screen.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['retry_key']:
                    logging.info("Retry key pressed. Restarting game.")
                    return  # Return to main, avoids recursive call to main
                elif event.key == settings.CONTROL_SETTINGS['quit_key']:
                    logging.info("Quit key pressed on Game Over Screen.")
                    pygame.quit()
                    sys.exit()


def pause_game(screen, font):
    """Pauses the game and waits until the player resumes."""
    paused = True
    pause_text = font.render("Paused. Press P to Resume.", True, settings.WHITE)
    screen.blit(pause_text, (settings.WIDTH // 2 - pause_text.get_width() // 2, settings.HEIGHT // 2))
    pygame.display.flip()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event detected while game is paused.")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == settings.CONTROL_SETTINGS['pause_key']:
                    logging.info("Resume key pressed. Resuming game.")
                    paused = False


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
