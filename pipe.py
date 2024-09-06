import pygame
import random
import numpy as np
from settings import *
from q_blackhole import QBlackHole
from q_aurorabor import AuroraBorealis

class Pipe:
    def __init__(self, x, speed=PIPE_SPEED):
        self.x = x
        self.speed = speed
        self.type = random.choice(['pipe', 'blackhole', 'aurora', 'laser_gate', 'thermal_detonator', 'tie_fighter'])

        if self.type == 'pipe':
            self.init_pipe()
        elif self.type == 'blackhole':
            self.init_blackhole()
        elif self.type == 'aurora':
            self.init_aurora()
        elif self.type == 'laser_gate':
            self.init_laser_gate()
        elif self.type == 'thermal_detonator':
            self.init_thermal_detonator()
        elif self.type == 'tie_fighter':
            self.init_tie_fighter()

    def init_pipe(self):
        self.gap_size = random.randint(PIPE_GAP - 30, PIPE_GAP + 30)
        self.gap_start = random.randint(50, WINDOW_HEIGHT - self.gap_size - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_start)
        self.bottom_rect = pygame.Rect(self.x, self.gap_start + self.gap_size, PIPE_WIDTH, WINDOW_HEIGHT - self.gap_start - self.gap_size)
        self.oscillation_offset = random.randint(0, 100)
        self.rotation_angle = random.randint(-5, 5)
        self.color = random.choice([PIPE_COLOR, (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 128)])
        self.has_hazard = random.random() < 0.15
        self.hazard_color = (255, 69, 0)
        self.has_power_up = random.random() < 0.15
        self.power_up_type = random.choice(["score", "slowdown", "shrink", "shield", "lightsaber"])
        self.power_up_color = (255, 255, 0)
        self.power_up_rect = pygame.Rect(self.x + PIPE_WIDTH // 4, self.gap_start + self.gap_size // 2 - 10, 20, 20)
        self.time_elapsed = 0

    def init_blackhole(self):
        self.entity = QBlackHole(self.x, self.speed)

    def init_aurora(self):
        self.entity = AuroraBorealis(self.x, self.speed)

    def init_laser_gate(self):
        self.height = random.randint(100, 150)
        self.gap_start = random.randint(50, WINDOW_HEIGHT - self.height - 50)
        self.top_rect = pygame.Rect(self.x, self.gap_start, PIPE_WIDTH, 5)
        self.bottom_rect = pygame.Rect(self.x, self.gap_start + self.height, PIPE_WIDTH, 5)
        self.color = (255, 0, 0)
        self.oscillation_offset = random.randint(0, 100)

    def init_thermal_detonator(self):
        self.rect = pygame.Rect(self.x, random.randint(50, WINDOW_HEIGHT - 50), 30, 30)
        self.color = (255, 69, 0)
        self.exploded = False

    def init_tie_fighter(self):
        self.image = pygame.image.load('assets/tie_fighter.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = random.randint(50, WINDOW_HEIGHT - self.rect.height - 50)
        self.laser_timer = 0
        self.laser_speed = 10
        self.lasers = []

    def update(self, bird, screen):
        if self.type == 'pipe':
            self.update_pipe()
        elif self.type == 'blackhole' or self.type == 'aurora':
            self.entity.update()
        elif self.type == 'laser_gate':
            self.update_laser_gate()
        elif self.type == 'thermal_detonator':
            self.update_thermal_detonator(bird, screen)
        elif self.type == 'tie_fighter':
            self.update_tie_fighter(bird)

    def update_pipe(self):
        self.x -= self.speed
        self.time_elapsed += 1
        self.oscillate_pipes()
        self.animate_pipes()
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        self.power_up_rect.x = self.x + PIPE_WIDTH // 4

    def update_laser_gate(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        self.oscillate_laser_gate()

    def update_thermal_detonator(self, bird, screen):
        self.x -= self.speed
        self.rect.x = self.x
        if not self.exploded and self.rect.colliderect(bird.rect):
            self.exploded = True
            self.trigger_explosion(bird, screen)

    def update_tie_fighter(self, bird):
        self.x -= self.speed
        self.rect.x = self.x
        self.laser_timer += 1
        if self.laser_timer > 30:
            self.shoot_laser()
            self.laser_timer = 0
        self.update_lasers(bird)

    def oscillate_pipes(self):
        oscillation = int(10 * (np.sin((self.x + self.oscillation_offset) * 0.05) + np.sin(self.time_elapsed * 0.1)))
        self.top_rect.y = self.gap_start + oscillation
        self.bottom_rect.y = self.gap_start + self.gap_size + oscillation

    def oscillate_laser_gate(self):
        oscillation = int(5 * np.sin(self.oscillation_offset + self.x * 0.1))
        self.top_rect.y += oscillation
        self.bottom_rect.y += oscillation

    def animate_pipes(self):
        pulse = int(5 * np.sin(self.time_elapsed * 0.1))
        self.top_rect.height += pulse
        self.bottom_rect.height += pulse

        if self.has_hazard:
            hazard_extension = int(5 * np.sin(self.time_elapsed * 0.2))
            self.top_rect.height += hazard_extension
            self.bottom_rect.height += hazard_extension

        if self.power_up_type == "slowdown":
            self.power_up_color = (0, 0, 255)
        elif self.power_up_type == "shrink":
            self.power_up_color = (0, 255, 0)
        elif self.power_up_type == "shield":
            self.power_up_color = (255, 0, 255)
        elif self.power_up_type == "lightsaber":
            self.power_up_color = (0, 255, 255)

    def shoot_laser(self):
        laser_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 2 - 2, 20, 4)
        self.lasers.append(laser_rect)

    def update_lasers(self, bird):
        for laser in self.lasers:
            laser.x -= self.laser_speed
            if laser.colliderect(bird.rect):
                bird.rect.y = WINDOW_HEIGHT
            if laser.x < -laser.width:
                self.lasers.remove(laser)

    def draw(self, screen):
        if self.type == 'pipe':
            self.draw_pipe(screen)
        elif self.type == 'blackhole' or self.type == 'aurora':
            self.entity.draw(screen)
        elif self.type == 'laser_gate':
            self.draw_laser_gate(screen)
        elif self.type == 'thermal_detonator':
            self.draw_thermal_detonator(screen)
        elif self.type == 'tie_fighter':
            self.draw_tie_fighter(screen)

    def draw_pipe(self, screen):
        top_pipe_surface = pygame.Surface((PIPE_WIDTH, self.top_rect.height), pygame.SRCALPHA)
        bottom_pipe_surface = pygame.Surface((PIPE_WIDTH, self.bottom_rect.height), pygame.SRCALPHA)
        top_pipe_surface.fill(self.color)
        bottom_pipe_surface.fill(self.color)
    
        top_rotated = pygame.transform.rotate(top_pipe_surface, self.rotation_angle)
        bottom_rotated = pygame.transform.rotate(bottom_pipe_surface, self.rotation_angle)
    
        screen.blit(top_rotated, self.top_rect.topleft)
        screen.blit(bottom_rotated, self.bottom_rect.topleft)
    
        if self.has_hazard:
            pygame.draw.rect(screen, self.hazard_color, (self.top_rect.x, self.top_rect.y + self.top_rect.height - 5, self.top_rect.width, 5))
            pygame.draw.rect(screen, self.hazard_color, (self.bottom_rect.x, self.bottom_rect.y, self.bottom_rect.width, 5))
    
        if self.has_power_up:
            pygame.draw.rect(screen, self.power_up_color, self.power_up_rect)

    def draw_laser_gate(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)

    def draw_thermal_detonator(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def draw_tie_fighter(self, screen):
        screen.blit(self.image, self.rect)
        for laser in self.lasers:
            pygame.draw.rect(screen, RED, laser)

    def trigger_explosion(self, bird, screen):
        explosion_radius = 50
        pygame.draw.circle(screen, (255, 140, 0), self.rect.center, explosion_radius)
        if bird.rect.colliderect(self.rect.inflate(explosion_radius, explosion_radius)):
            bird.rect.y = WINDOW_HEIGHT

    def off_screen(self):
        if self.type in ['pipe', 'laser_gate', 'thermal_detonator', 'tie_fighter']:
            return self.x < -PIPE_WIDTH
        else:
            return self.entity.off_screen()

    def collide(self, bird):
        if self.type == 'pipe':
            if self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect):
                if self.has_hazard:
                    bird.rect.y = WINDOW_HEIGHT
                return True
            if self.has_power_up and self.power_up_rect.colliderect(bird.rect):
                self.has_power_up = False
                return self.power_up_type
        elif self.type == 'laser_gate':
            if self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect):
                bird.rect.y = WINDOW_HEIGHT
                return True
        elif self.type == 'thermal_detonator':
            if self.rect.colliderect(bird.rect) and not self.exploded:
                self.trigger_explosion(bird, screen)
                return True
        elif self.type == 'tie_fighter':
            if self.rect.colliderect(bird.rect):
                bird.rect.y = WINDOW_HEIGHT
                return True
            for laser in self.lasers:
                if laser.colliderect(bird.rect):
                    bird.rect.y = WINDOW_HEIGHT
                    return True
        else:
            return self.entity.collide(bird)
        return False

    def hit_by_laser(self, lasers):
        if self.type in ['pipe', 'laser_gate', 'thermal_detonator', 'tie_fighter']:
            for laser in lasers:
                if self.type == 'pipe':
                    if self.top_rect.colliderect(laser.rect) or self.bottom_rect.colliderect(laser.rect):
                        return True
                elif self.type == 'laser_gate':
                    if self.top_rect.colliderect(laser.rect) or self.bottom_rect.colliderect(laser.rect):
                        return True
                elif self.type == 'thermal_detonator':
                    if self.rect.colliderect(laser.rect):
                        self.trigger_explosion()
                        return True
                elif self.type == 'tie_fighter':
                    if self.rect.colliderect(laser.rect):
                        return True
        else:
            return self.entity.hit_by_laser(lasers)
        return False

    def increase_difficulty(self, increment):
        self.speed += increment
        if self.type == 'pipe':
            self.gap_size = max(self.gap_size - 5, 80)
        elif self.type == 'laser_gate':
            self.height = max(self.height - 10, 60)
