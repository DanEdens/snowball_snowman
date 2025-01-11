import os
import sys
import pytest
import pygame
from pygame.event import Event

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.player import Player
from game.snowman import Snowball
from game.world import World
import main  # Import the main game module

@pytest.fixture
def game_window():
    """Setup a game window for testing"""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((main.WIDTH, main.HEIGHT))
    yield screen
    pygame.quit()

def test_game_start_and_screenshot(game_window):
    """Test game initialization and play button click"""
    # Initial game state should be MENU
    assert main.game_state == main.MENU
    
    # Draw initial frame
    main.draw()
    
    # Take screenshot of menu
    os.makedirs('test_screenshots', exist_ok=True)
    pygame.image.save(game_window, 'test_screenshots/menu.png')
    
    # Simulate clicking the play button
    click_pos = (main.WIDTH // 2, 2 * main.HEIGHT // 3)  # Play button position
    click_event = Event(pygame.MOUSEBUTTONDOWN, {
        'pos': click_pos,
        'button': 1,
        'touch': False
    })
    
    # Process the click event
    pygame.event.post(click_event)
    main.handle_input()
    
    # Game state should change to PLAYING
    assert main.game_state == main.PLAYING
    assert main.player is not None, "Player should be created"
    
    # Draw game frame
    main.draw()
    
    # Take screenshot of game start
    pygame.image.save(game_window, 'test_screenshots/game_start.png')
    
    print("Screenshots saved in test_screenshots directory")

def test_snowball_growth():
    """Test that snowballs grow correctly while rolling"""
    snowball = Snowball(100, 100)
    initial_size = snowball.size
    
    # Start rolling
    snowball.is_rolling = True
    
    # Update a few times
    for _ in range(10):
        snowball.grow()
    
    assert snowball.size > initial_size, "Snowball should grow while rolling"
    assert snowball.size <= snowball.max_size, "Snowball shouldn't exceed max size"

def test_world_zones():
    """Test that world zones are created correctly"""
    width, height = 800, 600
    world = World(width, height)
    
    assert world.rolling_zone.width == width // 2, "Rolling zone should be half the screen width"
    assert world.building_zone.width == width // 2, "Building zone should be half the screen width"
    assert world.rolling_zone.height == height, "Rolling zone should be full screen height"
    assert world.building_zone.height == height, "Building zone should be full screen height"

def test_player_movement():
    """Test player movement"""
    player = Player(100, 100)
    initial_x = player.position.x
    initial_y = player.position.y
    
    # Move right
    player.move(1, 0)
    assert player.position.x > initial_x, "Player should move right"
    
    # Move down
    player.move(0, 1)
    assert player.position.y > initial_y, "Player should move down"

def test_snowball_placement():
    """Test snowball placement in building zone"""
    width, height = 800, 600
    world = World(width, height)
    player = Player(width * 3/4, height/2)  # Place player in building zone
    
    # Start rolling a snowball
    player.start_rolling(world)
    assert player.rolling_snowball is None, "Should not be able to start rolling in building zone"
    
    # Move to rolling zone
    player.position.x = width/4
    player.start_rolling(world)
    assert player.rolling_snowball is not None, "Should be able to start rolling in rolling zone"
    
    # Move back to building zone and place
    player.position.x = width * 3/4
    placed_ball = player.place_snowball(world)
    assert placed_ball is not None, "Should be able to place snowball in building zone"
    assert player.rolling_snowball is None, "Rolling snowball should be cleared after placing" 
