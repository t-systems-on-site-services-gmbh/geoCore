"""Module containing the class Profile"""

from functools import reduce
from qgis.core import Qgis, QgsMessageLog

class Profile:
    """Profile represents a petrographic drilling profile.
    This class contains all relevant data for drawing"""

    def __init__(self, name):
        """Initialize the profile"""
        self.x = 0.0
        self.y = 0.0 # in cm
        self.margin = 1 # margin for description
        self.name = name
        self.boxes = []

    def height(self):
        """Return the height of the profile"""
        return reduce(lambda x, y: x + y, [b.height for b in self.boxes])

    def paint(self, scene):
        """Paint boxes onto scene"""
        self._paintName(scene)
        for b in self.boxes:
            b.paint(scene, self.x)

    def paintDescription(self, scene):
        """Paint description
        A profile drawing with description consists of
        three columns. The left column contains the heights
            - surface height above sea level (unit mNHN),
            - depth of the drilling (unit mNHN).
        The middle column contains the painted layer boxes.
        In the right column you'll find the heights of the
        individual layers (unit cm) relative to the surface height
        as well as a description of the layer's petrology.
        """
        self._paintRightDescription(scene)
        self._paintLeftDescription(scene)

    def _paintName(self, scene):
        """Paint the profile's name"""
        if len(self.boxes) == 0:
            return

        n = scene.addText(self.name)
        n.adjustSize()
        n.setX(self.x * 10) # cm to mm
        n.setY(-self.y * 10 - n.boundingRect().height())

    def _paintLeftDescription(self, scene):
        """Paint left column of the description"""
        if len(self.boxes) == 0:
            return

        yTop = self.y
        top = scene.addText("{:5.3n} mNHN".format(yTop / 100))
        top.adjustSize()
        xpos = (self.x * 10) - top.textWidth() - (self.margin * 10) # cm to mm
        ypos = -yTop * 10 # cm to mm
        top.setX(xpos)
        top.setY(ypos - 2) 
        scene.addLine(xpos, ypos, 10 * (self.x - self.margin), ypos)

        yBottom = self.y - self.height()
        bottom = scene.addText("{:5.3n} mNHN".format(yBottom / 100))
        bottom.adjustSize()
        xpos = (self.x * 10) - bottom.textWidth() - (self.margin * 10) # cm to mm
        ypos = -yBottom * 10 - (bottom.boundingRect().height() - 2)# cm to mm
        bottom.setX(xpos)
        bottom.setY(ypos)
        ypos = -yBottom * 10
        scene.addLine(xpos, ypos, 10 * (self.x - self.margin), ypos)

    def _paintRightDescription(self, scene):
        """Paint the right column of the description."""
        # x-position on the right
        w = max(self.boxes, key=lambda b: b.width)
        if w is not None:
            w = w.width
        else:
            w = 20
        xpos = self.x + w + self.margin

        for b in self.boxes:
            b.paintDescription(scene, xpos)
