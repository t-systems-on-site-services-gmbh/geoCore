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


class Otbp:
    """Otbp stands for object to be painted and is the
    base class for all objects (e.g. profiles, connectors and gauges)
    that will be painted later on."""

    def __init__(self):
        """Initialize the connector"""
        self._xFac = 1.0
        self._yFac = 1.0

    def setXFac(self, xFac):
        """Set scaling factor for x-position"""
        self._xFac = xFac

    def setYFac(self, yFac):
        """Set scaling factor for y-dimension"""
        self._yFac = yFac

    def partsHeights(self):
        """Return the height of the object"""
        return 0

    def paint(self, scene):
        """Paint the object onto the scene"""
        pass

    def paintDescription(self, scene):
        """Paint the object's description"""
        pass
