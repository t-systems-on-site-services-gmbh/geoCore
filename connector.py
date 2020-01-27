"""Module containing the class Connector"""

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
