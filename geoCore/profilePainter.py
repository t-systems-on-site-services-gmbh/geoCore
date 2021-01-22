""" This module contains the class profile Painter

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

class ProfilePainter:
    """This class is used to construct the graphics items"""

    def __init__(self, scene, viewHeight):
        """Initialize ProfilePainter.
        All constructed items are added to the given scene."""
        self.scene = scene
        self._viewHeight = viewHeight
        self._xFac = 1.0
        self._yFac = 1.0
        self._doAutoScale = True

    def applyScale(self, xFac, yFac):
        """Apply scaling factors in x- and y-dimension
        If None no scaling is applied for the x-position (i.e. xFac = 1.0)
        but auto-scaling for the height (y-dimension) is turned on."""
        if xFac is None:
            self._xFac = 1.0
        else:
            self._xFac = xFac

        if yFac is None:
            self._yFac = 1.0
            self._doAutoScale = True
        else:
            self._yFac = yFac
            self._doAutoScale = False

    def paint(self, otbps, addDescription):
        """Construct items.
        The parameter otbps stands for "objects to be painted"
        (i.e. profiles and connectors). Parameter addDescription
        denotes if a description shall be added."""
        if self._doAutoScale:
            self._setAutoYFac(otbps)
        for i in otbps:
            i.setXFac(self._xFac)
            i.setYFac(self._yFac)
            i.paint(self.scene)
            if addDescription:
                i.paintDescription(self.scene)

    def _setAutoYFac(self, otbps):
        """Set a smart scaling factor for the y-dimension"""
        facs = [ self._determineYFac(o) for o in otbps ]
        facsShrink = [ s for s in facs if s < 1.0 ]
        facsStretch = [ s for s in facs if s >= 1.0 ]

        self._yFac = 1.0

        if (len(facsShrink) > 0) and (len(facsStretch) > 0):
            self._yFac = 1.0
        elif len(facsShrink) > 0:
            self._yFac = max(facsShrink)
        elif len(facsStretch) > 0:
            self._yFac = min(facsStretch)

    def _determineYFac(self, otbp):
        """Determine a smart scaling factor for the y-dimension"""
        margin = 10
        vh = (self._viewHeight - margin) / 28.35 # pixel to cm
        facsShrink = [ vh / h for h in otbp.partsHeights() if h > vh and h != 0 ]
        facsStretch = [ vh / h for h in otbp.partsHeights() if h <= vh and h != 0 ]

        if len(facsShrink) > 0:
            return max(facsShrink)
        elif len(facsStretch) > 0:
            return min(facsStretch)
        else:
            return 1.0
