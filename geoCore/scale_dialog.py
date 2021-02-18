# -*- coding: utf-8 -*-
"""
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
import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin
# with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
     os.path.dirname(__file__), 'scale_dialog_base.ui'))

class ScaleDialog(QtWidgets.QDialog, FORM_CLASS):
    """Dialog to provide the scaling factors for x- and y-dimension"""

    def __init__(self, xFac, yFac, parent=None):
        """Constructor."""
        super(ScaleDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self._initControls(xFac, yFac)

    def _initControls(self, xFac, yFac):
        """Initialize the controls"""
        self.xAuto.toggled.connect(self._toggledXFactor)
        self.yAuto.toggled.connect(self._toggledYFactor)
        if xFac is None:
            self.xAuto.setChecked(True)
            self.xFactor.setEnabled(False)
        else:
            self.xAuto.setChecked(False)
            self.xFactor.setValue(xFac)
        if yFac is None:
            self.yAuto.setChecked(True)
            self.yFactor.setEnabled(False)
        else:
            self.yAuto.setChecked(False)
            self.yFactor.setValue(yFac)

    def _toggledXFactor(self, enabled):
        """Enable/disable xFactor spinbox"""
        self.xFactor.setEnabled(not enabled)

    def _toggledYFactor(self, enabled):
        """Enable/disable yFactor spinbox"""
        self.yFactor.setEnabled(not enabled)

    def xFac(self):
        """Get xFac"""
        if self.xAuto.isChecked():
            return None
        return self.xFactor.value()

    def yFac(self):
        """Get yFac"""
        if self.yAuto.isChecked():
            return None
        return self.yFactor.value()
