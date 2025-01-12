import os
import sys
import pytest
import pygame
from pygame.event import Event
import tempfile
import shutil

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set up command line arguments for agent mode
sys.argv.extend(['--agent'])

from game.player import Player
from game.snowman import Snowball, Snowman
from game.world import World
import main  # Import the main game module

@pytest.fixture
def game_window():
    """Setup a game window for testing"""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((main.WIDTH, main.HEIGHT))
    # Load assets
    main.play_button_img = pygame.image.load(os.path.join('src', 'images', 'play_button.png'))
    main.play_button_rect = main.play_button_img.get_rect()
    main.play_button_rect.centerx = main.WIDTH // 2
    main.play_button_rect.centery = 2 * main.HEIGHT // 3
    yield screen
    pygame.quit()

def test_game_start_and_screenshot(game_window):
    """Test game initialization and screenshot capture"""
    try:
        # Initialize game
        main.init_game()
        print("\nGame initialized")

        # Create a temporary directory for screenshots
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Created temporary directory: {temp_dir}")

            try:
                # Draw and save menu screenshot
                print("\nSaving menu screenshot...")
                game_window.fill(main.BLACK)
                main.draw_screen(game_window)
                pygame.display.flip()
                menu_path = os.path.join(temp_dir, 'menu.png')
                pygame.image.save(game_window, menu_path)
                if os.path.exists(menu_path):
                    print(f"Menu screenshot saved successfully: {menu_path}")
                    print(f"Size: {os.path.getsize(menu_path)} bytes")
                else:
                    raise FileNotFoundError(f"Failed to save menu screenshot at {menu_path}")

                # Start game and save game screenshot
                print("\nSaving game screenshot...")
                main.set_game_state(main.PLAYING)
                main.player = main.Player(main.WIDTH // 2, main.HEIGHT // 2)
                game_window.fill(main.BLACK)
                main.draw_screen(game_window)
                pygame.display.flip()
                game_path = os.path.join(temp_dir, 'game_start.png')
                pygame.image.save(game_window, game_path)
                if os.path.exists(game_path):
                    print(f"Game screenshot saved successfully: {game_path}")
                    print(f"Size: {os.path.getsize(game_path)} bytes")
                else:
                    raise FileNotFoundError(f"Failed to save game screenshot at {game_path}")

                # Create test_screenshots directory in project root
                print("\nSetting up test_screenshots directory...")
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                screenshots_dir = os.path.join(project_root, 'test_screenshots')
                if not os.path.exists(screenshots_dir):
                    os.makedirs(screenshots_dir)
                    print(f"Created directory: {screenshots_dir}")
                else:
                    print(f"Directory already exists: {screenshots_dir}")

                # Copy screenshots from temp directory
                print("\nCopying screenshots to test_screenshots directory...")
                for src, dst_name in [(menu_path, 'menu.png'), (game_path, 'game_start.png')]:
                    dst = os.path.join(screenshots_dir, dst_name)
                    try:
                        shutil.copy2(src, dst)
                        print(f"Copied {src} -> {dst}")
                        if os.path.exists(dst):
                            print(f"Verified copy exists: {dst} ({os.path.getsize(dst)} bytes)")
                        else:
                            raise FileNotFoundError(f"Failed to copy {dst_name}")
                    except Exception as e:
                        print(f"Error copying {dst_name}: {str(e)}")
                        raise

                # List contents of screenshots directory
                print("\nFinal contents of test_screenshots directory:")
                for item in os.listdir(screenshots_dir):
                    item_path = os.path.join(screenshots_dir, item)
                    print(f"- {item} ({os.path.getsize(item_path)} bytes)")

            except Exception as e:
                print(f"\nError during screenshot operations: {str(e)}")
                raise

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        raise

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

def test_snowball_stacking():
    """Test snowball stacking mechanics"""
    # Create two snowballs of different sizes
    big_ball = Snowball(100, 100)
    small_ball = Snowball(100, 50)

    # Make big ball bigger
    big_ball.size = 50
    small_ball.size = 30

    # Test stacking conditions
    assert small_ball.can_stack_on(big_ball), "Small ball should be able to stack on big ball"
    assert not big_ball.can_stack_on(small_ball), "Big ball should not stack on small ball"

    # Test stacking
    assert small_ball.stack_on(big_ball), "Stacking should succeed"
    assert small_ball.stacked_on == big_ball, "Small ball should reference big ball"
    assert big_ball.stacked_by == small_ball, "Big ball should reference small ball"

    # Test position updating
    small_ball.update(small_ball.position)
    expected_y = big_ball.position.y - big_ball.size - small_ball.size
    assert abs(small_ball.position.y - expected_y) < 0.1, "Small ball should be positioned above big ball"

def test_invalid_stacking():
    """Test invalid stacking scenarios"""
    ball1 = Snowball(100, 100)
    ball2 = Snowball(100, 50)
    ball3 = Snowball(100, 0)

    # Make all balls the same size
    ball1.size = ball2.size = ball3.size = 30

    # Test stacking same-sized balls
    assert not ball2.can_stack_on(ball1), "Same-sized balls should not stack"

    # Test stacking on already stacked ball
    ball2.stack_on(ball1)
    assert not ball3.can_stack_on(ball1), "Cannot stack on ball that already has something stacked"

    # Test unstacking
    ball2.unstack()
    assert ball1.stacked_by is None, "Ball1 should not have anything stacked on it"
    assert ball2.stacked_on is None, "Ball2 should not be stacked on anything"

def test_snowman_completion():
    """Test building a complete snowman"""
    # Create three snowballs of decreasing size
    base = Snowball(100, 100)
    middle = Snowball(100, 50)
    head = Snowball(100, 0)

    # Set appropriate sizes
    base.size = 60
    middle.size = 40
    head.size = 20

    # Create snowman with base
    snowman = Snowman(base)
    assert not snowman.is_complete, "New snowman should not be complete"

    # Add middle ball
    assert snowman.add_ball(middle), "Should be able to add middle ball"
    assert snowman.middle == middle, "Middle ball should be set"
    assert not snowman.is_complete, "Snowman with two balls should not be complete"

    # Add head
    assert snowman.add_ball(head), "Should be able to add head"
    assert snowman.head == head, "Head should be set"
    assert snowman.is_complete, "Snowman with three balls should be complete"

    # Try adding another ball
    extra_ball = Snowball(100, -50)
    extra_ball.size = 10
    assert not snowman.add_ball(extra_ball), "Should not be able to add ball to complete snowman"

def test_snowman_size_requirements():
    """Test size requirements for snowman building"""
    base = Snowball(100, 100)
    same_size = Snowball(100, 50)
    bigger = Snowball(100, 0)

    # Set sizes
    base.size = 40
    same_size.size = 40
    bigger.size = 50

    # Create snowman
    snowman = Snowman(base)

    # Try adding same-sized ball
    assert not snowman.add_ball(same_size), "Should not be able to add same-sized ball"

    # Try adding bigger ball
    assert not snowman.add_ball(bigger), "Should not be able to add bigger ball"

def test_game_start_and_screenshot():
    """Test game start and screenshot functionality"""
    # Initialize game
    main.init_game()

    # Check initial state
    assert main.get_game_state() == main.MENU

    # Draw initial frame and save screenshot
    main.draw()

    # Simulate clicking play button
    button_center = (main.WIDTH // 2, 2 * main.HEIGHT // 3)
    main.on_mouse_down(button_center)
    assert main.get_game_state() == main.PLAYING

    # Draw game frame and save screenshot
    main.draw()
