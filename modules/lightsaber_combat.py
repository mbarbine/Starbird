# modules/lightsaber_combat.py

import pygame
from modules.settings import *
from modules.sound_utils import play_sound_effect


def lightsaber_duel(event, screen, score=0):
    """
    Handles lightsaber duels based on player input.

    Args:
        event (pygame.event.Event): The key event for player input.
        screen (pygame.Surface): The game screen surface to draw on.
        score (int, optional): Current score of the player. Default is 0.

    Returns:
        int: Updated score after the duel action.
    """
    success = False
    action_text = ""
    color = WHITE

    # Map key events to actions
    if event.key == pygame.K_LEFT:
        action_text = "Block Left!"
        color = BLUE
        play_sound_effect('lightsaber')  # Play sound effect for action
        success = True
    elif event.key == pygame.K_RIGHT:
        action_text = "Block Right!"
        color = BLUE
        play_sound_effect('lightsaber')
        success = True
    elif event.key == pygame.K_UP:
        action_text = "Attack!"
        color = GREEN
        play_sound_effect('lightsaber')
        success = True
    else:
        action_text = "Missed!"
        color = RED
        play_sound_effect('collision')
    
    # Update score based on action success
    score += 10 if success else -5

    # Render action text on the screen
    font = pygame.font.Font(None, 50)
    text_surface = font.render(action_text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    
    # Small delay for feedback visibility
    pygame.time.wait(500)  # Adjust duration for better feedback experience

    return score


def display_duel_instructions(screen):
    """
    Displays instructions for the lightsaber duel on the screen.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.
    """
    instructions = [
        "Press LEFT to Block Left",
        "Press RIGHT to Block Right",
        "Press UP to Attack",
    ]
    font = pygame.font.Font(None, 40)
    y_offset = 100

    # Render each instruction line on the screen
    for line in instructions:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 50

    pygame.display.flip()
    pygame.time.wait(2000)  # Display instructions for 2 seconds


# Example usage (can be removed when integrated with the main game):
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lightsaber Duel")

    score = 0
    running = True

    display_duel_instructions(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                score = lightsaber_duel(event, screen, score)
                print(f"Current Score: {score}")

    pygame.quit()
