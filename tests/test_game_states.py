"""
Tests for game state management
"""
import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import game modules
import main

@pytest.fixture(autouse=True)
def setup_game():
    """Setup and reset game state before each test"""
    main.init_game()
    yield
    main.init_game()  # Reset after test

def test_state_constants():
    """Test that game states are properly defined"""
    assert main.MENU == 'menu'
    assert main.PLAYING == 'playing'
    assert main.CELEBRATION == 'celebration'

def test_initial_state():
    """Test that game starts in MENU state"""
    assert main.get_game_state() == main.MENU

def test_state_transition_to_playing():
    """Test transition from menu to playing state"""
    assert main.get_game_state() == main.MENU
    # Click in the center of the play button
    button_center = (main.WIDTH // 2, 2 * main.HEIGHT // 3)
    main.on_mouse_down(button_center)
    assert main.get_game_state() == main.PLAYING

def test_state_transition_to_celebration():
    """Test transition to celebration state"""
    main.set_game_state(main.PLAYING)
    assert main.get_game_state() == main.PLAYING
    main.set_game_state(main.CELEBRATION)
    assert main.get_game_state() == main.CELEBRATION

def test_invalid_state_transition():
    """Test that we can't transition from celebration to menu"""
    main.set_game_state(main.CELEBRATION)
    main.on_mouse_down((0, 0))  # Should not change state
    assert main.get_game_state() == main.CELEBRATION 
