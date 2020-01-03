"""Module containing the class Profile"""

from functools import reduce
from qgis.core import Qgis, QgsMessageLog

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

    def paint(self, scene):
        """Paint boxes onto scene"""
        for b in self.boxes:
            b.paint(scene, self.x)

    def paintDescription(self, scene):
        """Paint description"""
        w = max(self.boxes, key=lambda b: b.width)
        if w is not None:
            w = w.width
        else:
            w = 20
        xpos = self.x + w + 1
        for b in self.boxes:
            b.paintDescription(scene, xpos)
