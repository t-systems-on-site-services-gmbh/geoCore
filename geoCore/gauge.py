""" This module contains the class profile Painter

    geoCore - a QGIS plugin for drawing drilling profiles
    Copyright (C) 2021  Gerrit Bette, T-Systems on site services GmbH

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

from math import fabs
from .orientation import Orientation
from qgis.core import Qgis, QgsMessageLog
import math

class Gauge:
    """Gauge represents the gauge on the left or bottom of the drawing.
    This class contains all relevant data for drawing"""

    def __init__(self, x, y, minV, maxV, orientation):
        """Initialize the connector"""
        self._x = x
        self._y = y
        self._min = minV
        self._max = maxV
        self._xFac = 1.0
        self._yFac = 1.0
        self._width = 1
        self._orientation = orientation
        
        if minV % 10 != 0:
            self._min = math.trunc(minV / 10) * 10
        if maxV % 10 != 0:
            self._max = (math.trunc(maxV / 10) + 1) * 10

    def setXFac(self, xFac):
        """Set scaling factor for x-position"""
        self._xFac = xFac

    def setYFac(self, yFac):
        """Set scaling factor for y-dimension"""
        self._yFac = yFac

    def partsHeights(self):
        """Return the height of the gauge"""
        if self._orientation == Orientation.VERTICAL:
            return [fabs(self._max - self._min)]
        else:
            return [self._width]

    def paint(self, scene):
        """Paint the guage onto the scene"""
        if self._orientation == Orientation.VERTICAL:
            self._paintVertical(scene)            
        else:
            self._paintHorizontal(scene)            

    def _paintHorizontal(self, scene):
        w = fabs(self._max - self._min) * self._xFac * 10
        x = self._x * self._xFac * 10
        y = (-self._y * self._yFac) * 10 + 70
        scene.addRect(x, y, w, self._width * 10)

        y = y + (self._width + 1) * 10
        scene.addLine(x, y, x, y + 20)
        n = scene.addText("{:.2f} m".format(float(self._min) / 100))
        n.adjustSize()
        n.setX(x - n.boundingRect().width() / 2)
        n.setY(y + 20 + 1)

        x = x + w
        scene.addLine(x, y, x, y + 20)
        n = scene.addText("{:.2f} m".format(float(self._max) / 100))
        n.adjustSize()
        n.setX(x - n.boundingRect().width() / 2)
        n.setY(y + 20 + 1)

    def _paintVertical(self, scene):
        h = -fabs(self._max - self._min) * self._yFac * 10
        x = self._x * self._xFac * 10 - 80
        y = -self._y * self._yFac * 10

        scene.addRect(x, y, self._width * 10, h)

        x = x - 10
        y = y + h
        n = scene.addText("{:.2f} m".format(float(self._min) / 100))
        n.adjustSize()
        xLeft = x - n.textWidth()
        n.setX(xLeft)
        n.setY(y)
        scene.addLine(xLeft, y, x, y)
        
        y = y - h
        n = scene.addText("{:.2f} m".format(float(self._min) / 100))
        n.adjustSize()
        n.setX(xLeft)
        n.setY(y - n.boundingRect().height() - 2)
        scene.addLine(xLeft, y, x, y)
        
        # QgsMessageLog.logMessage("x {}, y {}, min {}, max {}".format(x, y, self._min, self._max), level=Qgis.Info)

    def paintDescription(self, scene):
        """Paint the gauge's description"""
        # nothing to paint
        pass
