import pygame
import sys
import numpy as np  # Import NumPy for efficient calculations
from modules.bird import Bird
from modules.pipe import Pipe
from modules.backgrounds import ScrollingBackground
from modules.settings import *
from modules.q_blackhole import QBlackHole
from modules.q_aurorabor import AuroraBorealis

class Laser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 2)  # Laser dimensions
        self.speed = LASER_SPEED

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, LASER_COLOR, self.rect)  # Red lasers

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            score = f.read().strip()
            return int(score) if score.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def start_screen(screen):
    screen.fill(START_SCREEN_COLOR)
    draw_text(screen, "STARBIRD", 64, BIRD_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    draw_text(screen, "Press SPACE or UP to Start", 22, BIRD_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def game_over_screen(screen, score):
    screen.fill(GAME_OVER_COLOR)
    draw_text(screen, "GAME OVER", 64, BIRD_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    draw_text(screen, f"Score: {score}", 22, BIRD_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    draw_text(screen, "Press SPACE or UP to Restart", 22, BIRD_COLOR, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
    pygame.display.flip()
    save_high_score(score)
    wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return

def main():
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer before loading sounds
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Starbird")
    clock = pygame.time.Clock()

    # Load Sounds
    flap_sound = pygame.mixer.Sound(FLAP_SOUND)
    score_sound = pygame.mixer.Sound(SCORE_SOUND)
    hit_sound = pygame.mixer.Sound(HIT_SOUND)
    laser_sound = pygame.mixer.Sound(LASER_SOUND)  # Laser sound

    # Background
    background = ScrollingBackground()

    start_screen(screen)

    # Slowdown control variables
    slowdown = False
    slowdown_timer = 0

    # Shield effect
    shield_active = False
    shield_timer = 0

    while True:
        bird = Bird()
        obstacles = []
        for i in range(3):
            x_position = WINDOW_WIDTH + i * (PIPE_WIDTH + 200)
            obstacle_type = np.random.choice(['pipe', 'blackhole', 'AuroraBorealis'], p=[0.7, 0.15, 0.15])
            if obstacle_type == 'pipe':
                obstacles.append(Pipe(x_position))
            elif obstacle_type == 'blackhole':
                obstacles.append(QBlackHole(x_position))
            elif obstacle_type == 'AuroraBorealis':
                obstacles.append(AuroraBorealis(x_position))
                
        lasers = []
        score = 0
        high_score = load_high_score()
        difficulty_increment = 0
        flap_cooldown = 0
        laser_cooldown = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_UP] and flap_cooldown == 0:
                        bird.flap()
                        flap_sound.play()
                        flap_cooldown = FLAP_COOLDOWN_TIME
                    if event.key == pygame.K_LCTRL and laser_cooldown == 0:  # Shoot laser with K_LCTRL
                        laser_sound.play()
                        lasers.append(Laser(bird.rect.right, bird.rect.centery))
                        laser_cooldown = LASER_COOLDOWN_TIME

            if flap_cooldown > 0:
                flap_cooldown -= 1

            if laser_cooldown > 0:
                laser_cooldown -= 1

            if slowdown:
                if slowdown_timer > 0:
                    slowdown_timer -= 1
                else:
                    slowdown = False

            if shield_active:
                if shield_timer > 0:
                    shield_timer -= 1
                else:
                    shield_active = False

            bird.update()
            background.update()

            for laser in lasers:
                laser.update()

            lasers = [laser for laser in lasers if laser.rect.x < WINDOW_WIDTH]

            for obstacle in obstacles:
                obstacle.update(bird, screen)  # Pass bird to obstacle updates

                if obstacle.collide(bird):
                    if not shield_active:
                        hit_sound.play()
                        game_over_screen(screen, score)
                        break

                if obstacle.off_screen():
                    obstacles.remove(obstacle)
                    x_position = WINDOW_WIDTH + PIPE_WIDTH
                    obstacle_type = np.random.choice(['pipe', 'blackhole', 'AuroraBorealis'], p=[0.7, 0.15, 0.15])
                    if obstacle_type == 'pipe':
                        obstacles.append(Pipe(x_position, speed=(PIPE_SPEED + difficulty_increment)))
                    elif obstacle_type == 'blackhole':
                        obstacles.append(QBlackHole(x_position))
                    elif obstacle_type == 'AuroraBorealis':
                        obstacles.append(AuroraBorealis(x_position))
                    score += 1
                    score_sound.play()

                    # Increase difficulty every 5 points
                    if score % 5 == 0:
                        difficulty_increment += DIFFICULTY_INCREASE

                if obstacle.hit_by_laser(lasers):
                    obstacles.remove(obstacle)
                    score += 5  # Extra points for destroying an obstacle with a laser
                    score_sound.play()

            else:
                # Continue game loop
                background.draw(screen)
                bird.draw(screen)
                for obstacle in obstacles:
                    obstacle.draw(screen)
                for laser in lasers:
                    laser.draw(screen)

                # Draw shield around bird if active
                if shield_active:
                    pygame.draw.circle(screen, SHIELD_COLOR, bird.rect.center, BIRD_WIDTH // 2 + 10, 3)

                # Display score in white
                draw_text(screen, f"Score: {score}", 36, (255, 255, 255), 70, 10)
                draw_text(screen, f"High Score: {high_score}", 24, (255, 255, 255), WINDOW_WIDTH - 100, 10)

                pygame.display.flip()
                clock.tick(FPS)
                continue

            break  # Exit loop if a collision occurs

if __name__ == "__main__":
    main()
