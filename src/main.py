"""
Snowball Snowman - A creative puzzle game about building snowmen!
"""
import os
import pygame
from pygame import Rect, Surface
from game.player import Player
from game.snowman import Snowball
from game.world import World

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

# Current game state
game_state = MENU

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snowball Snowman")
clock = pygame.time.Clock()

# Load play button
play_button_img = pygame.image.load(os.path.join('src', 'images', 'play_button.png'))
play_button_rect = play_button_img.get_rect(center=(WIDTH // 2, 2 * HEIGHT // 3))

# Game objects
player = None
active_snowball = None
world = World(WIDTH, HEIGHT)
placed_snowballs = []

def draw_menu():
    """Draw the main menu with title and play button"""
    # Draw title
    font = pygame.font.Font(None, 60)
    title = font.render("Snowball Snowman", True, (0, 0, 128))  # Navy blue
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(title, title_rect)
    
    # Draw play button
    screen.blit(play_button_img, play_button_rect)
    pygame.draw.rect(screen, (255, 0, 0), play_button_rect, 1)  # Debug outline

def draw_game():
    """Draw the main game screen"""
    world.draw(screen)
    
    if player:
        screen.blit(player.actor._surf, player.actor._surf.get_rect(center=player.position))
        if player.rolling_snowball:
            player.rolling_snowball.draw(screen)
    
    for snowball in placed_snowballs:
        snowball.draw(screen)

def draw():
    """Draw the current game state"""
    screen.fill((255, 255, 255))  # White background
    
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == CELEBRATION:
        pass  # TODO: Implement celebration
    
    pygame.display.flip()

def handle_input():
    """Handle keyboard and mouse input"""
    global game_state, player
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == MENU:
            if play_button_rect.collidepoint(event.pos):
                game_state = PLAYING
                player = Player(WIDTH // 2, HEIGHT // 2)
                print("Game started!")
    
    if game_state == PLAYING and player:
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        player.move(dx, dy)
        
        if keys[pygame.K_SPACE]:
            player.start_rolling(world)
        elif player.rolling_snowball:
            placed = player.place_snowball(world)
            if placed:
                placed_snowballs.append(placed)
        
        if player.rolling_snowball:
            player.rolling_snowball.update(player.position)
    
    return True

def main():
    """Main game loop"""
    running = True
    while running:
        running = handle_input()
        draw()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == '__main__':
    main()
