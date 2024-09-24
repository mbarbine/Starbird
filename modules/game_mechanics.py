from modules.screen_utils import (
    init_game_window,
    start_screen,
    game_over_screen,
    pause_game
)
from modules.sound_utils import (
    load_sound,
    play_background_music
)
from modules.score_utils import (
    save_high_scores,
    load_high_scores,
    get_player_name,
    update_leaderboard
)
from modules.draw_utils import (
    draw_game_elements,
    draw_hud
)
from modules.game_mechanics import (
    update_obstacles_with_dt,
    check_collisions,
    handle_collision,
    handle_game_mechanics
)
