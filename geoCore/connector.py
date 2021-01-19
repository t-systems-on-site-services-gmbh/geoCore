""" Module containing the class Connector

    geoCore - a QGIS plugin for drawing drilling profiles
    Copyright (C) 2019 - 2021  Gerrit Bette, T-Systems on site services GmbH

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

from qgis.core import Qgis, QgsMessageLog
from math import fabs

class Connector:
    """Connector represents the line connecting two petrographic
    drilling profiles.
    This class contains all relevant data for drawing"""

    def __init__(self):
        """Initialize the connector"""
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0 # in cm
        self.xOffset = 0.0
        self._xFac = 1.0
        self._yFac = 1.0

    def setXFac(self, xFac):
        """Set scaling factor for x-position"""
        self._xFac = xFac

    def setYFac(self, yFac):
        """Set scaling factor for y-dimension"""
        self._yFac = yFac

    def partsHeights(self):
        """Return the height of each connector"""
        return [fabs(self.y1 - self.y2)]

    def paint(self, scene):
        """Paint connector onto scene"""
        # convert from cm to mm
        # direction of y-axis it top down, i.e. point (0,0) is in the upper left
        scene.addLine((self.x1 * self._xFac + self.xOffset) * 10, 
            self.y1 * self._yFac * -10, 
            self.x2 * self._xFac * 10, 
            self.y2 * self._yFac * -10)

    def paintDescription(self, scene):
        """Paint the connector's description"""
        # nothing to paint
        pass
