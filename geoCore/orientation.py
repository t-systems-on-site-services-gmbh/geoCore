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

from enum import Enum, auto

class Orientation(Enum):
    """Enum for the orientation vertical/horizontal"""

    VERTICAL = auto()
    HORIZONTAL = auto()
