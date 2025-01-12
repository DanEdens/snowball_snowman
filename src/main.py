"""
Snowball Snowman - A creative puzzle game about building snowmen!
"""
import os
import sys
import argparse
import pygame
from pygame import Rect, Surface
from game.player import Player
from game.snowman import Snowball
from game.world import World
from game.snowman import Snowman

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--agent', action='store_true', help='Enable agent mode for automated testing')

# Only parse args if script is run directly
if __name__ == '__main__':
    args = parser.parse_args()
    DEBUG_AUTO_CLOSE = args.agent
else:
    # For testing, create a mock args object
    class Args:
        def __init__(self):
            self.agent = False
    args = Args()

# Initialize pygame
pygame.init()
pygame.font.init()

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Game states
MENU = 'menu'
PLAYING = 'playing'
CELEBRATION = 'celebration'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0, 100)  # Semi-transparent green for stacking indicator

# Debug settings
AGENT_MODE = args.agent  # True if running in agent/test mode
DEBUG_START_TIME = pygame.time.get_ticks()  # Get the start time

# Game state variables
_game_state = MENU  # Start in menu state
player = None
active_snowball = None
placed_snowballs = []
snowmen = []

def get_game_state():
    """Get the current game state"""
    global _game_state
    return _game_state

def set_game_state(state):
    """Set the game state"""
    global _game_state
    _game_state = state

def init_game():
    """Initialize the game state"""
    global _game_state, player, active_snowball, placed_snowballs, snowmen
    set_game_state(MENU)
    player = None
    active_snowball = None
    placed_snowballs = []
    snowmen = []

def reset_game():
    """Reset the game objects without changing state"""
    global player, active_snowball, placed_snowballs, snowmen
    player = None
    active_snowball = None
    placed_snowballs = []
    snowmen = []

def handle_mouse_click(pos):
    """Handle mouse click events"""
    if get_game_state() == MENU:
        if play_button_rect.collidepoint(pos):
            set_game_state(PLAYING)
            global player
            player = Player(WIDTH // 2, HEIGHT // 2)
            print("Game started!")

def on_mouse_down(pos):
    """Handle mouse down event (compatibility wrapper)"""
    handle_mouse_click(pos)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snowball Snowman")
clock = pygame.time.Clock()

# Load play button
play_button_img = pygame.image.load(os.path.join('src', 'images', 'play_button.png'))
play_button_rect = play_button_img.get_rect()
play_button_rect.centerx = WIDTH // 2
play_button_rect.centery = 2 * HEIGHT // 3

# Game objects
world = World(WIDTH, HEIGHT)

def draw_menu(screen):
    """Draw the main menu with Snowball Snowman title and play button"""
    screen.fill(BLACK)
    
    # Draw title
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Snowball Snowman", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    # Draw play button
    screen.blit(play_button_img, play_button_rect)
    
    # Draw debug outline for play button in agent mode
    if AGENT_MODE:
        pygame.draw.rect(screen, (255, 0, 0), play_button_rect, 1)

def update():
    """Update game state"""
    if get_game_state() == PLAYING:
        handle_input()

def draw_screen(screen):
    """Draw the current game state"""
    if get_game_state() == MENU:
        draw_menu(screen)
    elif get_game_state() == PLAYING:
        draw_game(screen)

def handle_input():
    """Handle keyboard input for the game"""
    global player, placed_snowballs, snowmen
    
    # Auto-close after 5 seconds in agent mode
    if AGENT_MODE and pygame.time.get_ticks() - DEBUG_START_TIME > 5000:
        print("Agent mode: Auto-closing after 5 seconds")
        return False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and get_game_state() == MENU:
            if play_button_rect.collidepoint(event.pos):
                set_game_state(PLAYING)
                player = Player(WIDTH // 2, HEIGHT // 2)
                print("Game started!")
    
    if get_game_state() == PLAYING and player:
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        player.move(dx, dy)
        
        if keys[pygame.K_SPACE]:
            player.start_rolling(world)
        elif player.rolling_snowball:
            placed = player.place_snowball(world)
            if placed:
                # Try to stack the snowball
                stackable = find_stackable_snowball(placed, placed_snowballs, snowmen)
                if stackable:
                    placed.stack_on(stackable)
                    print("Stacked snowball!")
                    
                    # Check if this creates or adds to a snowman
                    added_to_snowman = False
                    for snowman in snowmen:
                        if stackable in snowman.all_balls:
                            snowman.add_ball(placed)
                            added_to_snowman = True
                            if snowman.is_complete:
                                print("Snowman completed!")
                                if get_game_state() != CELEBRATION:
                                    set_game_state(CELEBRATION)
                            break
                    
                    if not added_to_snowman and not stackable.stacked_on:
                        # Start a new snowman with these balls
                        snowmen.append(Snowman(stackable))
                        snowmen[-1].add_ball(placed)
                
                placed_snowballs.append(placed)
        
        # Update all snowballs
        if player.rolling_snowball:
            player.rolling_snowball.update(player.position)
        for snowball in placed_snowballs:
            snowball.update(snowball.position)
    
    return True

def draw_game(screen):
    """Draw the game screen with player, snowballs, and zones"""
    # Draw world zones
    pygame.draw.rect(screen, world.rolling_zone_color, world.rolling_zone)
    pygame.draw.rect(screen, world.building_zone_color, world.building_zone)
    
    # Draw zone labels
    font = pygame.font.Font(None, 36)
    snowball_text = font.render("SNOWBALL", True, (255, 0, 0))  # Red
    snowman_text = font.render("SNOWMAN", True, (0, 100, 0))  # Dark green
    
    screen.blit(snowball_text, (world.width//4 - snowball_text.get_width()//2, 30))
    screen.blit(snowman_text, (3*world.width//4 - snowman_text.get_width()//2, 30))
    
    # Draw player
    if player:
        player.draw(screen)
        if player.rolling_snowball:
            # Draw snowball
            pygame.draw.circle(
                screen,
                WHITE,
                (int(player.rolling_snowball.position.x), int(player.rolling_snowball.position.y)),
                int(player.rolling_snowball.size)
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (int(player.rolling_snowball.position.x), int(player.rolling_snowball.position.y)),
                int(player.rolling_snowball.size),
                1  # Line width
            )
            
            # Draw stacking indicator if near a stackable ball
            if world.building_zone.collidepoint(player.position):
                stackable = find_stackable_snowball(player.rolling_snowball, placed_snowballs, snowmen)
                if stackable:
                    # Draw green circle around stackable ball
                    pygame.draw.circle(
                        screen,
                        GREEN,
                        (int(stackable.position.x), int(stackable.position.y)),
                        int(stackable.size + 5)  # Slightly larger than the ball
                    )
    
    # Draw placed snowballs and snowmen
    for snowball in placed_snowballs:
        pygame.draw.circle(
            screen,
            WHITE,
            (int(snowball.position.x), int(snowball.position.y)),
            int(snowball.size)
        )
        pygame.draw.circle(
            screen,
            BLACK,
            (int(snowball.position.x), int(snowball.position.y)),
            int(snowball.size),
            1  # Line width
        )
        
        # Draw completion indicator for complete snowmen
        for snowman in snowmen:
            if snowman.is_complete and snowball in snowman.all_balls:
                pygame.draw.circle(
                    screen,
                    (200, 255, 200),  # Light green
                    (int(snowball.position.x), int(snowball.position.y)),
                    int(snowball.size + 2),
                    1  # Line width
                )

# Initialize screen
screen = None

def init_screen():
    """Initialize the game screen"""
    global screen
    if not screen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    return screen

def draw():
    """Draw the current game state (compatibility wrapper)"""
    global screen
    if not screen:
        screen = init_screen()
    draw_screen(screen)

def main():
    """Main game loop"""
    global game_state
    pygame.init()
    pygame.font.init()
    screen = init_screen()
    pygame.display.set_caption("Snowball Snowman")
    
    # Initialize game state
    init_game()
    
    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
        
        update()
        draw_screen(screen)
        pygame.display.flip()
        clock.tick(60)
        
        if DEBUG_AUTO_CLOSE and pygame.time.get_ticks() - start_time > 5000:
            print("Debug: Auto-closing after 5 seconds")
            running = False
    
    pygame.quit()

def find_stackable_snowball(new_ball, placed_balls, snowmen):
    """Find a snowball that the new ball can stack on"""
    # First check existing snowmen for incomplete stacks
    for snowman in snowmen:
        if not snowman.is_complete:
            stackable = snowman.get_stackable_ball()
            if stackable and new_ball.can_stack_on(stackable):
                return stackable
    
    # Then check for new potential base balls
    # Sort balls by size (largest first) to prefer stacking on larger balls
    unattached_balls = [b for b in placed_balls if not b.stacked_on and not b.stacked_by]
    sorted_balls = sorted(unattached_balls, key=lambda b: b.size, reverse=True)
    
    for ball in sorted_balls:
        if new_ball.can_stack_on(ball):
            return ball
    return None

if __name__ == '__main__':
    main()
