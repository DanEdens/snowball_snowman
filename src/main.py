"""
Snowball Snowman - A creative puzzle game about building snowmen!
"""
import pgzrun

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Game states
MENU = 'menu'
PLAYING = 'playing'
CELEBRATION = 'celebration'

# Current game state
game_state = MENU

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
    """Draw the main menu"""
    screen.draw.text(
        "Snowball Snowman",
        centerx=WIDTH//2,
        centery=HEIGHT//3,
        fontsize=60,
        color="navy"
    )
    screen.draw.text(
        "Click to Start",
        centerx=WIDTH//2,
        centery=2*HEIGHT//3,
        fontsize=30,
        color="black"
    )

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
        game_state = PLAYING

def update():
    """Update game logic"""
    pass

pgzrun.go()  # Start the game
