import pygame

def create_player_sprite():
    """Create a simple circular player sprite"""
    surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(surface, (0, 0, 255), (16, 16), 16)  # Blue circle
    return surface
