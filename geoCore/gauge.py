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

from math import fabs, trunc
from .orientation import Orientation
from .otbp import Otbp
from qgis.PyQt.QtGui import QBrush, QColor, QPen

class Gauge(Otbp):
    """Gauge represents the gauge on the left or bottom of the drawing.
    This class contains all relevant data for drawing"""

    def __init__(self, x, y, minV, maxV, orientation):
        """Initialize the connector"""
        self._x = x
        self._y = y
        self._min = minV
        self._max = maxV
        self._width = 0.5
        self._orientation = orientation
        
        if minV % 10 != 0:
            self._min = trunc(minV / 10) * 10
        if maxV % 10 != 0:
            self._max = (trunc(maxV / 10) + 1) * 10

        w = self._max - self._min
        self._stepWidth = w / 5
        if self._stepWidth % 10 != 0:
            if self._stepWidth % 10 < 5:
                self._stepWidth = trunc(self._stepWidth / 10) * 10
            else:
                self._stepWidth = (trunc(self._stepWidth / 10) + 1) * 10
            self._max = self._min + 5 * self._stepWidth

    def partsHeights(self):
        """Return the height of the gauge"""
        if self._orientation == Orientation.VERTICAL:
            return [fabs(self._max - self._min)]
        else:
            return [self._width + 1, 5]

    def paint(self, scene):
        """Paint the guage onto the scene"""
        if self._orientation == Orientation.VERTICAL:
            self._paintVertical(scene)
        else:
            self._paintHorizontal(scene)

    def _paintHorizontal(self, scene):
        """Paint the horizontal gauge"""
        w = fabs(self._max - self._min) * self._xFac * 10
        x = self._x * self._xFac * 10
        y = (-self._y * self._yFac) * 10 + 70

        self._paintHorizontalDescription(scene, x, y, w)

        pen, bBrush, wBrush = self._getPenAndBrush()
        sw = self._stepWidth * self._xFac * 10
        scene.addRect(x, y, sw, self._width * 10, pen, bBrush)
        scene.addRect(x + sw, y, sw, self._width * 10, pen, wBrush)
        scene.addRect(x + 2 * sw, y, sw, self._width * 10, pen, bBrush)
        scene.addRect(x + 3 * sw, y, sw, self._width * 10, pen, wBrush)
        scene.addRect(x + 4 * sw, y, sw, self._width * 10, pen, bBrush)

    def _paintHorizontalDescription(self, scene, x, y, w):
        """Paint the description of the horizontal gauge"""
        # left
        y = y + (self._width + 1) * 10
        scene.addLine(x, y, x, y + 20)
        n = scene.addText("{:.2f} m".format(float(self._min) / 100))
        n.adjustSize()
        n.setX(x - n.boundingRect().width() / 2)
        n.setY(y + 20 + 1)

        # right
        x = x + w
        scene.addLine(x, y, x, y + 20)
        n = scene.addText("{:.2f} m".format(float(self._max) / 100))
        n.adjustSize()
        n.setX(x - n.boundingRect().width() / 2)
        n.setY(y + 20 + 1)

    def _paintVertical(self, scene):
        """Pain the vertial gauge"""
        h = -fabs(self._max - self._min) * self._yFac * 10
        x = self._x * self._xFac * 10 - 80
        y = -self._y * self._yFac * 10

        self._paintVerticalDescription(scene, x, y, h)

        pen, bBrush, wBrush = self._getPenAndBrush()
        sw = -self._stepWidth * self._yFac * 10
        scene.addRect(x, y, self._width * 10, sw, pen, bBrush)
        scene.addRect(x, y + 1 * sw, self._width * 10, sw, pen, wBrush)
        scene.addRect(x, y + 2 * sw, self._width * 10, sw, pen, bBrush)
        scene.addRect(x, y + 3 * sw, self._width * 10, sw, pen, wBrush)
        scene.addRect(x, y + 4 * sw, self._width * 10, sw, pen, bBrush)

    def _paintVerticalDescription(self, scene, x, y, h):
        """Paint the description of the vertical gauge"""
        # top
        x = x - 10
        y = y + h
        n = scene.addText("{:.2f} m".format(float(self._max) / 100))
        n.adjustSize()
        xLeft = x - n.textWidth()
        n.setX(xLeft)
        n.setY(y)
        scene.addLine(xLeft, y, x, y)
        
        # bottom
        y = y - h
        n = scene.addText("{:.2f} m".format(float(self._min) / 100))
        n.adjustSize()
        n.setX(xLeft)
        n.setY(y - n.boundingRect().height() - 2)
        scene.addLine(xLeft, y, x, y)

    def _getPenAndBrush(self):
        """Get the pen and brush"""
        pen = QPen()
        blackBrush = QBrush(QColor("black"))
        whiteBrush = QBrush(QColor("white"))
        return pen, blackBrush, whiteBrush
