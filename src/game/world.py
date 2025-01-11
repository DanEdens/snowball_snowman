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
