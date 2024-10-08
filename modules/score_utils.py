# modules/score_utils.py

import logging
import os
import pygame
import sys  # Import sys to handle sys.exit()
import modules.settings as settings

def save_high_scores(high_scores):
    """Saves the high scores to a file."""
    try:
        with open(settings.HIGH_SCORE_FILE, 'w') as f:
            f.write(f"{high_scores['player']}:{high_scores['top_score']}\n")
        logging.info("High scores saved successfully.")
    except IOError as e:
        logging.error(f"Error saving high scores: {e}")

def load_high_scores():
    """Loads the high scores from a file."""
    high_scores = {'player': 'None', 'top_score': 0}
    try:
        with open(settings.HIGH_SCORE_FILE, 'r') as f:
            line = f.readline().strip()
            if line:
                player, score = line.split(':')
                high_scores['player'] = player
                high_scores['top_score'] = int(score)
                logging.info(f"High score loaded: {high_scores['top_score']} by {high_scores['player']}")
    except FileNotFoundError:
        logging.warning(f"High score file {settings.HIGH_SCORE_FILE} not found. Creating a new one.")
        save_high_scores(high_scores)
    except ValueError:
        logging.error("High score file is corrupted. Resetting to default values.")
        save_high_scores(high_scores)
    except Exception as e:
        logging.error(f"Error loading high scores: {e}")
    return high_scores

def get_player_name(screen):
    """
    Prompts the player to enter their name.

    Args:
        screen (pygame.Surface): The screen surface to display the input box.

    Returns:
        str: The player's name or "Player1" if no input is provided.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(settings.WIDTH // 2 - 100, settings.HEIGHT // 2, 200, 50)
    color_inactive = settings.COLORS.get('WHITE', (255, 255, 255))
    color_active = settings.COLORS.get('BLUE', (0, 0, 255))
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle the active variable if the box is clicked
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(settings.COLORS.get('GAME_OVER', (128, 0, 0)))  # Default color if not defined in settings
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
    
    return text if text else "Player1"

def update_leaderboard(screen, score, high_scores):
    """
    Updates the leaderboard with the current score.

    Args:
        screen (pygame.Surface): The screen surface for displaying the input box if a new high score is achieved.
        score (int): The current score.
        high_scores (dict): The high score data to be updated.
    """
    if score > high_scores['top_score']:
        high_scores['top_score'] = score
        high_scores['player'] = get_player_name(screen)
        save_high_scores(high_scores)
        logging.info(f"New high score achieved: {score} by {high_scores['player']}")
