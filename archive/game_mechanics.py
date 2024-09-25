# game_mechanics.py
from modules.screen_utils import pause_game
from modules.sound_utils import play_sound_effect
from modules.level_loader import load_level, handle_level_progression
from modules.game_utils import update_score, check_game_over

def update_game_state(screen, bird, obstacles, quantum_elements, score, level_config, dt):
    """
    Handles the core game state updates including bird movement, obstacle updates, and score tracking.
    """
    bird.update_with_dt(dt)
    update_obstacles_with_dt(obstacles, dt)
    score = update_score(bird, obstacles, score)
    
    if check_collisions(bird, obstacles, quantum_elements):
        handle_collision(bird, play_sound_effect("collision"))
        if check_game_over(bird):
            game_over_screen(screen, bird, score)
            return False, score

    return True, score

def handle_special_events(bird, screen, event_timers):
    """
    Manages special game events like Jedi Training, Dark Side, and Hyperspace.
    """
    if event_timers['jedi_training'] <= 0 and random.random() < settings.EVENT_FREQUENCY['jedi_training']:
        if jedi_training(screen):
            bird.apply_power_up("shield")
        event_timers['jedi_training'] = settings.EVENT_COOLDOWNS['jedi_training']
    # Additional events like 'dark_side' and 'hyperspace' can be managed similarly
