import pygame
from settings import *
from q_blackhole import QBlackHole
from q_aurorabor import AuroraBorealis

class Bird:
    def __init__(self):
        self.images = [pygame.image.load(frame).convert_alpha() for frame in BIRD_FRAMES]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = BIRD_START_X
        self.rect.y = BIRD_START_Y
        self.velocity = 0.0  # Ensure this is initialized as a float
        self.acceleration = GRAVITY
        self.air_resistance = AIR_RESISTANCE
        self.rotation_angle = 0
        self.is_flapping = False
        self.max_velocity = MAX_VELOCITY
        self.flap_cooldown = 0
        self.flap_cooldown_time = FLAP_COOLDOWN_TIME
        self.shield_active = False
        self.shield_duration = SHIELD_DURATION
        self.laser_cooldown = LASER_COOLDOWN_TIME
        self.pulse_offset = 0  # For shield pulsing effect
        self.color = BIRD_COLOR  # Base color of the bird
        self.superposition_active = False  # Future use for quantum superposition
        self.entanglement_linked = False  # Future use for quantum entanglement
        self.lightsaber_active = False  # New feature for lightsaber
        self.lightsaber_color = (0, 255, 0)  # Default lightsaber color (green)
        self.lightsaber_length = 50  # Length of the lightsaber

    def update(self):
        # Ensure both velocity and acceleration are floats
        self.velocity = float(self.velocity)
        self.acceleration = float(self.acceleration)

        # Apply gravity and air resistance
        self.velocity += self.acceleration
        self.velocity *= self.air_resistance
        self.velocity = min(self.velocity, self.max_velocity)
        self.rect.y += int(self.velocity)

        # Rotate bird based on velocity
        self.rotation_angle = min(max(-45, self.velocity * 2), 45)
        rotated_image = pygame.transform.rotate(self.images[int(self.current_frame)], self.rotation_angle)
        self.image = rotated_image

        # Update animation frame based on velocity
        self.current_frame += self.animation_speed * (1 + abs(self.velocity) / 10)
        if self.current_frame >= len(self.images):
            self.current_frame = 0

        # Flap cooldown management
        if self.flap_cooldown > 0:
            self.flap_cooldown -= 1

        # Laser cooldown management
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

        # Shield duration and pulsing effect
        if self.shield_active:
            self.shield_duration -= 1
            self.pulse_offset += 1  # Increase pulse offset for visual effect
            if self.shield_duration <= 0:
                self.shield_active = False
                self.shield_duration = SHIELD_DURATION
            if self.pulse_offset > 30:
                self.pulse_offset = 0  # Reset pulse effect

        # Quantum Superposition and Entanglement Handling
        if self.superposition_active:
            self.handle_quantum_superposition()
        if self.entanglement_linked:
            self.handle_quantum_entanglement()

        # Keep the bird within the screen bounds
        if self.rect.y <= 0:
            self.rect.y = 0
            self.velocity = max(self.velocity, 0)  # Prevents the bird from sticking to the top
        elif self.rect.y >= WINDOW_HEIGHT - BIRD_HEIGHT:
            self.rect.y = WINDOW_HEIGHT - BIRD_HEIGHT
            self.velocity = 0

    def flap(self):
        if self.flap_cooldown == 0:
            self.velocity = FLAP_STRENGTH * (1 + abs(self.velocity) * 0.1)
            self.is_flapping = True
            self.flap_cooldown = self.flap_cooldown_time

    def draw(self, screen):
        # Change bird color if shield is active
        if self.shield_active:
            self.color = (self.color[0], (self.color[1] + self.pulse_offset) % 255, (self.color[2] + self.pulse_offset) % 255)
        else:
            self.color = BIRD_COLOR

        tinted_image = self.image.copy()
        tinted_image.fill(self.color, special_flags=pygame.BLEND_MULT)
        screen.blit(tinted_image, self.rect)

        if self.shield_active:
            self.draw_shield(screen)

        if self.lightsaber_active:
            self.draw_lightsaber(screen)

    def draw_shield(self, screen):
        shield_color = tuple(min(255, max(0, c + self.pulse_offset)) for c in SHIELD_COLOR)
        pygame.draw.ellipse(screen, shield_color, self.rect.inflate(20, 20), 3)

    def draw_lightsaber(self, screen):
        # Draw the lightsaber extending from the bird
        start_pos = (self.rect.centerx, self.rect.centery)
        end_pos = (self.rect.centerx + self.lightsaber_length, self.rect.centery)
        pygame.draw.line(screen, self.lightsaber_color, start_pos, end_pos, 5)

    def activate_lightsaber(self):
        self.lightsaber_active = True

    def deactivate_lightsaber(self):
        self.lightsaber_active = False

    def quantum_flap(self):
        # Placeholder for CUDAQ-powered quantum flap
        pass

    def ai_behavior(self):
        # Placeholder for AI-driven movement
        pass

    def apply_power_up(self, power_up_type):
        if power_up_type == "shrink":
            self.rect.height = int(self.rect.height * 0.8)
            self.rect.width = int(self.rect.width * 0.8)
        elif power_up_type == "shield":
            self.shield_active = True
            self.shield_duration = SHIELD_DURATION  # Reset shield duration
        elif power_up_type == "slowdown":
            self.air_resistance = 0.9
        elif power_up_type == "score":
            pass  # Placeholder for score power-up effect
        elif power_up_type == "lightsaber":
            self.activate_lightsaber()

    def reset_power_ups(self):
        self.air_resistance = AIR_RESISTANCE
        self.shield_active = False
        self.lightsaber_active = False
        self.rect.height = BIRD_HEIGHT
        self.rect.width = BIRD_WIDTH

    def quantum_superposition(self):
        # Placeholder for implementing quantum superposition in bird's state
        self.superposition_active = True

    def handle_quantum_superposition(self):
        # Logic for handling bird's behavior in a superposition state
        pass

    def quantum_entanglement(self):
        # Placeholder for implementing quantum entanglement in game mechanics
        self.entanglement_linked = True

    def handle_quantum_entanglement(self):
        # Logic for handling quantum entanglement with other game entities
        pass

    def quantum_error_correction(self):
        # Placeholder for implementing quantum error correction algorithms
        pass

    def quantum_walk(self):
        # Placeholder for implementing quantum random walk for bird's movement
        pass

    def quantum_optimization(self):
        # Placeholder for implementing quantum optimization algorithms (VQE, QAOA)
        pass

    def quantum_circuit_optimization(self):
        # Placeholder for quantum circuit optimization
        pass
