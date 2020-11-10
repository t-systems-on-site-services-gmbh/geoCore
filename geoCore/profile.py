""" Module containing the class Profile

    geoCore - a QGIS plugin for drawing drilling profiles
    Copyright (C) 2019, 2020  Gerrit Bette, T-Systems on site services GmbH

    This file is part of geoCore.

    geoCore is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    geoCore is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with geoCore.  If not, see <https://www.gnu.org/licenses/>.
"""

from functools import reduce
from qgis.core import Qgis, QgsMessageLog

class Profile:
    """Profile represents a petrographic drilling profile.
    This class contains all relevant data for drawing"""

    def __init__(self, name):
        """Initialize the profile"""
        self.x = 0.0
        self.y = 0.0 # in cm
        self._yFac = 1.0
        self.margin = 1 # margin for description
        self.name = name
        self.boxes = []

    def height(self):
        """Return the height of the profile"""
        return reduce(lambda x, y: x + y, [b.height for b in self.boxes])

    def setYFac(self, yFac):
        """Set scaling factor for y-dimension"""
        self._yFac = yFac
        for b in self.boxes:
            b.setYFac(yFac)

    def paint(self, scene):
        """Paint boxes onto scene"""
        self._paintName(scene)
        self._paintLegend(scene)
        for b in self.boxes:
            b.paint(scene, self.x)

    def _paintLegend(self, scene):
        """Paint legend explaining the width of the individual 
        layers/boxes below the profile"""
        yBottom = self.y - self.height()
        yPos = (yBottom - self.margin) * self._yFac * -10 # cm to mm
        for b in self.boxes:
            xPos = (self.x + b.width) * 10
            scene.addLine(xPos, yPos, xPos, yPos + 20)
            n = scene.addText(b.name)
            n.adjustSize()
            n.setX(xPos - n.boundingRect().width() / 2)
            n.setY(yPos + 20 + self.margin)

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

        n = scene.addText("{}".format(self.name)) # name might be an int
        n.adjustSize()
        n.setX(self.x * 10) # cm to mm
        n.setY(-self.y * self._yFac * 10 - n.boundingRect().height())

    def _paintLeftDescription(self, scene):
        """Paint left column of the description"""
        if len(self.boxes) == 0:
            return

        yTop = self.y
        top = scene.addText("{:.2f} mNHN".format(float(yTop) / 100))
        top.adjustSize()
        xpos = (self.x * 10) - top.textWidth() - (self.margin * 10) # cm to mm
        ypos = -yTop * self._yFac * 10 # cm to mm
        top.setX(xpos)
        top.setY(ypos - 2) 
        scene.addLine(xpos, ypos, 10 * (self.x - self.margin), ypos)

        yBottom = self.y - self.height()
        bottom = scene.addText("{:.2f} mNHN".format(float(yBottom) / 100))
        bottom.adjustSize()
        xpos = (self.x * 10) - bottom.textWidth() - (self.margin * 10) # cm to mm
        ypos = -yBottom * self._yFac * 10 - (bottom.boundingRect().height() - 2) # cm to mm
        bottom.setX(xpos)
        bottom.setY(ypos)
        ypos = -yBottom * self._yFac * 10
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
