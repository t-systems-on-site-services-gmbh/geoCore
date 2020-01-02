"""Module containing the class Profile"""

from functools import reduce

class Profile:
    """Profile represents a petrographic drilling profile.
    This class contains all relevant data for drawing"""

    def __init__(self, name):
        """Initialize the profile"""
        self.x = 0.0
        self.y = 0.0
        self.name = name
        self.boxes = []

    def height(self):
        """Return the height of the profile"""
        return reduce(lambda x, y: x + y, [b.height for b in self.boxes])
