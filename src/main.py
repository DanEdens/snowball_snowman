"""
Snowball Snowman - A creative puzzle game about building snowmen!
"""
import pgzrun
import os
from pygame import Rect
from pgzero.actor import Actor

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Game states
MENU = 'menu'
PLAYING = 'playing'
CELEBRATION = 'celebration'

# Current game state
game_state = MENU

# Debug info
print(f"Current working directory: {os.getcwd()}")
print(f"Looking for image at: {os.path.join('images', 'play_button.png')}")

# Load play button
try:
    play_button = Actor('play_button')  # Pygame Zero will look in the images directory automatically
    print("Successfully loaded play button image")
except Exception as e:
    print(f"Error loading play button: {e}")

play_button.center = (WIDTH // 2, 2 * HEIGHT // 3)  # Position the button
print(f"Play button position: {play_button.center}")

def draw():
    """Called every frame to draw the game"""
    screen.fill('white')  # White background like snow

    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == CELEBRATION:
        draw_celebration()

def draw_menu():
    """Draw the main menu with title and play button"""
    # Draw title
    screen.draw.text(
        "Snowball Snowman",
        centerx=WIDTH//2,
        centery=HEIGHT//3,
        fontsize=60,
        color="navy"
    )

    # Draw play button and debug rectangle
    play_button.draw()
    screen.draw.rect(Rect(play_button.left, play_button.top, play_button.width, play_button.height), "red")  # Debug outline

def draw_game():
    """Draw the main game screen"""
    # TODO: Implement game drawing
    pass

def draw_celebration():
    """Draw the celebration animation"""
    # TODO: Implement celebration
    pass

def on_mouse_down(pos):
    """Handle mouse clicks"""
    global game_state
    if game_state == MENU:
        if play_button.collidepoint(pos):
            game_state = PLAYING
            print("Play button clicked!")

def update():
    """Update game logic"""
    pass

pgzrun.go()  # Start the game
