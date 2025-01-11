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

def test_initial_state():
    """Test that game starts in MENU state"""
    assert main.game_state == main.MENU

def test_state_constants():
    """Test that game states are properly defined"""
    assert main.MENU == 'menu'
    assert main.PLAYING == 'playing'
    assert main.CELEBRATION == 'celebration'

def test_window_dimensions():
    """Test that window dimensions are set correctly"""
    assert main.WIDTH == 800
    assert main.HEIGHT == 600

# Mock the screen object since we can't use actual Pygame in tests
class MockScreen:
    def __init__(self):
        self.draw = MockDraw()
        self.filled_color = None
    
    def fill(self, color):
        self.filled_color = color

class MockDraw:
    def __init__(self):
        self.texts = []
    
    def text(self, text, **kwargs):
        self.texts.append((text, kwargs))

@pytest.fixture
def mock_screen():
    return MockScreen()

def test_menu_drawing(mock_screen, monkeypatch):
    """Test menu text rendering"""
    # Replace the global screen with our mock
    monkeypatch.setattr(main, 'screen', mock_screen)
    
    # Call the menu drawing function
    main.draw_menu()
    
    # Check that the correct texts were drawn
    texts = mock_screen.draw.texts
    assert len(texts) == 2
    
    # Check title
    title_text, title_kwargs = texts[0]
    assert title_text == "Snowball Snowman"
    assert title_kwargs['fontsize'] == 60
    assert title_kwargs['color'] == "navy"
    
    # Check start prompt
    prompt_text, prompt_kwargs = texts[1]
    assert prompt_text == "Click to Start"
    assert prompt_kwargs['fontsize'] == 30
    assert prompt_kwargs['color'] == "black"

def test_state_transition():
    """Test state transition from menu to playing"""
    main.game_state = main.MENU
    main.on_mouse_down((0, 0))  # Click position doesn't matter for menu
    assert main.game_state == main.PLAYING 
