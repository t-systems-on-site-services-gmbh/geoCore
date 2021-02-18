""" This module defines the class Config

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

import os
import yaml

class Config:
    """Class providing configuration data for plugin. The callback function
    showMessage(title, message) is used to show error messages."""

    def __init__(self, showMessage):
        self.showMessage = showMessage
        self.myDir = os.path.dirname(__file__)

        self.settings = self._readConfig(os.path.join(self.myDir, "config", "config.yml"))
        self.geoCore = self._readConfig(os.path.join(self.myDir, "config/geoCore", "geoCore.yml"))

    def _readConfig(self, fileName):
        """Return a YML file's contents.
        The file is assumed to be encoded in utf-8"""
        try:
            with open(fileName, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.parser.ParserError as pe:
            self.showMessage("Error", "Failed to parse YML: {0}".format(pe))
        except FileNotFoundError:
            self.showMessage("Error", "File {0} was not found.".format(fileName))
