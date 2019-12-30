"""This module defines the class Config"""

import os
import yaml

class Config:
    """Class providing configuration data for plugin. The callback function
    showMessage(title, message) is used to show error messages."""

    def __init__(self, showMessage):
        self.showMessage = showMessage
        self.myDir = os.path.dirname(__file__)

        self.settings = self._readConfig(os.path.join(self.myDir, "./config.yml"))
        self.geoCore = self._readConfig(os.path.join(self.myDir, "geoCore", "geoCore.yml"))

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
