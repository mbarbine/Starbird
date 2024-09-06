import pygame
from settings import *
def jedi_training(screen, width, height, color_green):
    font = pygame.font.Font(None, 50)
    prompt = "Press the sequence: W, A, S, D"
    text_surface = font.render(prompt, True, color_green)
    screen.blit(text_surface, (width // 4, height // 2 - 100))
    pygame.display.flip()

    sequence = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    user_sequence = []

    while len(user_sequence) < len(sequence):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                user_sequence.append(event.key)
                if user_sequence != sequence[:len(user_sequence)]:
                    return False  # Failure

    return True  # Success
