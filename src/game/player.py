from pygame import Vector2, Surface, draw
from game.snowman import Snowball
import pygame

class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.speed = 5
        self.rolling_snowball = None
        # Create a temporary circle for the player
        self.surface = Surface((32, 32), pygame.SRCALPHA)
        draw.circle(self.surface, (0, 0, 255), (16, 16), 16)  # Blue circle
        
    def move(self, dx, dy):
        """Move the player based on input"""
        self.position.x += dx * self.speed
        self.position.y += dy * self.speed
        
    def draw(self, screen):
        """Draw the player"""
        rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, rect)
        
    def start_rolling(self, world):
        """Start rolling a new snowball"""
        if self.rolling_snowball is None and world.rolling_zone.collidepoint(self.position):
            self.rolling_snowball = Snowball(self.position.x, self.position.y)
            self.rolling_snowball.is_rolling = True
            
    def place_snowball(self, world):
        """Try to place the snowball in the building zone"""
        if (self.rolling_snowball and 
            world.building_zone.collidepoint(self.position)):
            placed_ball = self.rolling_snowball
            self.rolling_snowball = None
            return placed_ball
        return None
