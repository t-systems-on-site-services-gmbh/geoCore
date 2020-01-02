"""This module contains the class profile Painter"""

from qgis.PyQt import QtWidgets

class ProfilePainter:
    """This class is used to construct the graphics items"""

    def __init__(self, scene):
        """Initialize ProfilePainter.
        All constructed items are added to the scene."""
        self.scene = scene

    def paint(self, otps):
        """Construct items.
        otps stands for objects to be painted (i.e. profiles and connectors)."""
        self.scene.addRect(50, 50, 100, 200)
