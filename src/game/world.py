from pygame import Rect

class World:
    def __init__(self, width, height):
        # Create two zones - left for rolling, right for building
        self.width = width
        self.height = height
        
        # Define zones
        self.rolling_zone = Rect(0, 0, width // 2, height)
        self.building_zone = Rect(width // 2, 0, width // 2, height)
        
        # Zone colors for debug visualization
        self.rolling_zone_color = (200, 255, 200)  # Light green
        self.building_zone_color = (220, 255, 220)  # Slightly lighter green
        
    def draw(self, screen):
        """Draw the world zones"""
        screen.draw.filled_rect(self.rolling_zone, self.rolling_zone_color)
        screen.draw.filled_rect(self.building_zone, self.building_zone_color)
        
        # Draw zone labels
        screen.draw.text("SNOWBALL", centerx=self.width//4, centery=30, color="red")
        screen.draw.text("SNOWMAN", centerx=3*self.width//4, centery=30, color="darkgreen")
