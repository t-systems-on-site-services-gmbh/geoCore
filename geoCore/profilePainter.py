""" This module contains the class profile Painter

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

class ProfilePainter:
    """This class is used to construct the graphics items"""

    def __init__(self, scene):
        """Initialize ProfilePainter.
        All constructed items are added to the scene."""
        self.scene = scene

    def paint(self, otbps, description):
        """Construct items.
        The parameter otbps stands for "objects to be painted"
        (i.e. profiles and connectors). Parameter description
        denotes if a description shall be added."""
        yFac = self._determineYFac(otbps)
        for i in otbps:
            i.setYFac(yFac)
            i.paint(self.scene)
            if description:
                i.paintDescription(self.scene)

    def _determineYFac(self, otbps):
        """Determine a smart scaling factor for the y-dimension"""
        return 1.0