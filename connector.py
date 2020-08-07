""" Module containing the class Connector

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

from qgis.core import Qgis, QgsMessageLog

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

    def paint(self, scene):
        """Paint connector onto scene"""
        # convert from cm to mm
        # direction of y-axis it top down, i.e. point (0,0) is in the upper left
        scene.addLine(self.x1 * 10, self.y1 * -10, self.x2 * 10, self.y2 * -10)

    def paintDescription(self, scene):
        """Paint the connector's description"""
        # nothing to paint
        pass
