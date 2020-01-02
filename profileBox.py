"""Module containing the class ProfileBox"""

class ProfileBox:
    """ProfileBox represents one layer of a petrographic drilling profile.
    This class contains all relevant data for drawing"""

    def __init__(self, layer):
        """Initialize the box"""
        self.layer = layer
        self.group = self.layer
        self.y = 0.0
        self.width = 0.0
        self.height = 0.0
        self.info = ''
        self.color = ''
        self.texture = ''
        self.isFirst = layer == 1
        self.isLast = False
