import os
import sys
import pytest
import pygame

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from game.player import Player
from game.snowman import Snowball
from game.world import World

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
