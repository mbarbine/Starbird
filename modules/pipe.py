# modules/pipe.py

import pygame
import random
from modules.settings import (
    PIPE_WIDTH, PIPE_COLOR, PIPE_HEIGHT, PIPE_GAP, PIPE_VARIANT_COLORS, PIPE_SPEED, LEVEL_THRESHOLD, WIDTH
)

class Pipe:
    """
    Represents a pair of top and bottom pipes in the game.
    """

    def __init__(self, x, speed=PIPE_SPEED, pipe_gap=PIPE_GAP):
        """
        Initializes the Pipe instance.
        
        Args:
            x (int): The x-coordinate of the pipe.
            speed (int, optional): Movement speed of the pipe. Defaults to PIPE_SPEED.
            pipe_gap (int, optional): Gap between top and bottom pipes. Defaults to PIPE_GAP.
        """
        self.speed = speed
        self.pipe_gap = pipe_gap

        # Randomize top pipe height within a reasonable range
        top_height = random.randint(50, PIPE_HEIGHT - pipe_gap - 50)
        self.top_rect = pygame.Rect(x, 0, PIPE_WIDTH, top_height)

        # Bottom pipe height is determined based on the gap
        bottom_height = PIPE_HEIGHT - top_height - pipe_gap
        self.bottom_rect = pygame.Rect(x, PIPE_HEIGHT - bottom_height, PIPE_WIDTH, bottom_height)

        # Track if the pipe has been passed by the bird for scoring
        self.passed = False

        # Optional combined rect for enhanced collision handling (may not always be needed)
        self.collision_rect = pygame.Rect(x, 0, PIPE_WIDTH, PIPE_HEIGHT)

        # Assign a random color from the variants for visual variety
        self.color = random.choice(PIPE_VARIANT_COLORS)

    def update(self, dt):
        """
        Moves the pipe to the left based on its speed and delta time.

        Args:
            dt (float): Delta time to scale movement speed.
        """
        self.top_rect.x -= self.speed * dt * 60
        self.bottom_rect.x -= self.speed * dt * 60
        self.collision_rect.x -= self.speed * dt * 60

    def draw(self, screen):
        """
        Draws the top and bottom pipes on the screen.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)

    def off_screen(self):
        """
        Checks if the pipe has moved off the screen.

        Returns:
            bool: True if the pipe is off the screen, False otherwise.
        """
        return self.top_rect.right < 0

    def increase_speed(self, level):
        """
        Increases the speed of the pipes as the player progresses to higher levels.

        Args:
            level (int): The current level of the game.
        """
        self.speed += (level // LEVEL_THRESHOLD) * 0.5  # Increase speed slightly every few levels

    def adjust_gap(self, score):
        """
        Adjusts the gap between the pipes based on the current score.

        Args:
            score (int): The current score of the player.
        """
        if score % 50 == 0 and self.pipe_gap > 100:
            self.pipe_gap -= 5  # Reduce gap size slightly every 50 points

    def is_passed(self, bird):
        """
        Checks if the bird has passed the pipe.

        Args:
            bird (Bird): The bird object to check against.

        Returns:
            bool: True if the bird has passed the pipe, False otherwise.
        """
        if not self.passed and bird.rect.left > self.top_rect.right:
            self.passed = True
            return True
        return False

def add_pipe(obstacles, x_position):
    """
    Adds a new pipe to the list of obstacles.

    Args:
        obstacles (list): The list of current obstacles in the game.
        x_position (int): The x-coordinate to place the new pipe.
    """
    pipe = Pipe(x_position)
    obstacles.append(pipe)

def draw_pipes(screen, obstacles):
    """
    Draws all pipes in the obstacle list.

    Args:
        screen (pygame.Surface): The game screen to draw on.
        obstacles (list): The list of current obstacles in the game.
    """
    for obstacle in obstacles:
        if isinstance(obstacle, Pipe):
            obstacle.draw(screen)

def update_pipes(obstacles, dt):
    """
    Updates all pipes in the obstacle list.

    Args:
        obstacles (list): The list of current obstacles in the game.
        dt (float): Delta time to scale movement speed.
    """
    for obstacle in obstacles:
        if isinstance(obstacle, Pipe):
            obstacle.update(dt)

def remove_off_screen_pipes(obstacles):
    """
    Removes pipes that have moved off the screen.

    Args:
        obstacles (list): The list of current obstacles in the game.
    """
    obstacles[:] = [pipe for pipe in obstacles if not pipe.off_screen()]

def check_collision(bird, pipes):
    """
    Checks for collisions between the bird and the pipes.

    Args:
        bird (Bird): The bird object to check collision against.
        pipes (list): The list of pipe objects.

    Returns:
        bool: True if a collision is detected, False otherwise.
    """
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return True
    return False
