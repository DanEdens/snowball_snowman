from pygame import Vector2

class Snowball:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.size = 20  # Starting size in pixels
        self.min_size = 20
        self.max_size = 60
        self.growing_speed = 0.2
        self.is_rolling = False
        
    def grow(self):
        """Increase snowball size while rolling"""
        if self.is_rolling and self.size < self.max_size:
            self.size += self.growing_speed
    
    def update(self, player_pos):
        """Update snowball position to follow player"""
        if self.is_rolling:
            self.position = Vector2(player_pos)
            self.grow()
    
    def draw(self, screen):
        """Draw the snowball"""
        screen.draw.filled_circle(
            (self.position.x, self.position.y),
            int(self.size),
            'white'
        )
        screen.draw.circle(
            (self.position.x, self.position.y),
            int(self.size),
            'black'
        )
