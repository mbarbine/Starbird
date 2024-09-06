import pygame
import random
import numpy as np
from settings import *

class AuroraBorealis:
    def __init__(self, x, speed=PIPE_SPEED):
        self.x = x
        self.height = random.randint(150, 250)  # Taller aurora for a dramatic effect
        self.width = random.randint(150, 250)   # Wider aurora for increased difficulty
        self.y = random.randint(50, WINDOW_HEIGHT - self.height - 50)
        self.speed = speed
        self.colors = [self.generate_random_color() for _ in range(5)]
        self.color_change_timer = 0
        self.glow_intensity = 1.0
        self.quantum_chaos_active = False
        self.chaos_timer = 0
        self.update_gradient()

    def generate_random_color(self):
        """Generate a vibrant, neon-like color."""
        return random.choice([(0, 255, 255), (255, 0, 255), (0, 255, 0), (255, 255, 0), (0, 128, 255), (255, 69, 0)])

    def update_gradient(self):
        """Create a vertical gradient with a glowing effect."""
        self.gradient_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(self.height):
            color_index = i * len(self.colors) // self.height
            color = tuple(max(0, min(255, int(c * self.glow_intensity))) for c in self.colors[color_index])
            self.gradient_surface.fill(color, rect=pygame.Rect(0, i, self.width, 1))

    def activate_quantum_chaos(self):
        """Activate quantum chaos, altering the aurora's properties randomly."""
        self.quantum_chaos_active = True
        self.chaos_timer = random.randint(100, 200)  # Quantum chaos lasts for a random duration

    def update(self, bird=None):
        """Update position, color, glow intensity, and handle quantum chaos."""
        self.x -= self.speed
        self.color_change_timer += 1

        if self.color_change_timer > 20:  # Quick color changes for vibrancy
            self.colors = [self.generate_random_color() for _ in range(5)]
            self.update_gradient()
            self.color_change_timer = 0

        # Pulse the aurora's glow intensity to simulate a glowing effect
        self.glow_intensity = 1 + 0.2 * np.sin(pygame.time.get_ticks() / 200.0)
        self.update_gradient()

        # Handle quantum chaos
        if self.quantum_chaos_active:
            self.chaos_timer -= 1
            if self.chaos_timer <= 0:
                self.quantum_chaos_active = False
                self.speed = PIPE_SPEED  # Reset speed after chaos
            else:
                self.quantum_chaos_effect()

        # Check for bird collision and apply effects
        if bird and self.collide(bird):
            self.apply_effect(bird)

    def quantum_chaos_effect(self):
        """Apply random effects during quantum chaos."""
        if random.random() < 0.1:  # 10% chance to flip direction
            self.speed *= -1
        if random.random() < 0.1:  # 10% chance to change height or width
            self.height = random.randint(100, 300)
            self.width = random.randint(100, 300)
        if random.random() < 0.1:  # 10% chance to teleport vertically
            self.y = random.randint(50, WINDOW_HEIGHT - self.height - 50)
        self.update_gradient()

    def draw(self, screen):
        """Draw the aurora with its glowing effect."""
        if self.gradient_surface:
            screen.blit(self.gradient_surface, (self.x, self.y))

    def off_screen(self):
        """Check if the aurora has moved off-screen."""
        return self.x < -self.width

    def collide(self, bird):
        """Check if the aurora collides with the bird."""
        aurora_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if aurora_rect.colliderect(bird.rect):
            return True
        return False

    def hit_by_laser(self, lasers):
        """Check if the aurora is hit by a laser."""
        aurora_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for laser in lasers:
            if aurora_rect.colliderect(laser.rect):
                return True
        return False

    def apply_effect(self, bird):
        """Apply a special effect if the bird collides with the aurora."""
        bird.velocity *= 0.5  # Slow down the bird as if it’s caught in the aurora’s magnetic field
        bird.rotation_angle += 15  # Add a visual spin to the bird for a disorienting effect
        bird.shield_active = False  # Deactivate the bird's shield if it has one

    def enhance_effects(self):
        """Enhance the visual and interactive effects of the aurora."""
        self.colors = [self.generate_random_color() for _ in range(10)]  # More colors for richer gradients
        self.speed += 0.5  # Increase speed slightly to add challenge
        self.glow_intensity = 1.5  # Make the glow more intense
        self.update_gradient()
