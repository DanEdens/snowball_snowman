from pygame import Vector2

class Snowball:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.size = 20  # Starting size in pixels
        self.min_size = 20
        self.max_size = 60
        self.growing_speed = 0.2
        self.is_rolling = False
        self.stacked_on = None  # Reference to snowball below this one
        self.stacked_by = None  # Reference to snowball above this one
        
    def grow(self):
        """Increase snowball size while rolling"""
        if self.is_rolling and self.size < self.max_size:
            self.size += self.growing_speed
    
    def update(self, player_pos):
        """Update snowball position to follow player"""
        if self.is_rolling:
            self.position = Vector2(player_pos)
            self.grow()
        elif self.stacked_on:
            # Update position to stay on top of the snowball below
            self.position = Vector2(
                self.stacked_on.position.x,
                self.stacked_on.position.y - self.stacked_on.size - self.size
            )
    
    def can_stack_on(self, other_ball):
        """Check if this snowball can stack on another"""
        if not other_ball or self.stacked_on or other_ball.stacked_by:
            return False
            
        # Size check - top ball should be smaller
        if self.size >= other_ball.size:
            return False
            
        # Position check - must be close enough to stack
        stack_distance = other_ball.size + self.size  # Distance between centers when stacked
        current_distance = self.position.distance_to(other_ball.position)
        
        return current_distance < stack_distance * 1.2  # Allow 20% margin for easier stacking
    
    def stack_on(self, other_ball):
        """Stack this snowball on top of another"""
        if not self.can_stack_on(other_ball):
            return False
            
        self.stacked_on = other_ball
        other_ball.stacked_by = self
        self.is_rolling = False
        return True
    
    def unstack(self):
        """Remove this snowball from its stack"""
        if self.stacked_on:
            self.stacked_on.stacked_by = None
            self.stacked_on = None
        if self.stacked_by:
            self.stacked_by.stacked_on = None
            self.stacked_by = None
