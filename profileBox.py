"""Module containing the class ProfileBox"""

#from qgis.PyQt import QtWidgets
from qgis.PyQt.QtGui import QBrush, QColor, QPen
from qgis.core import Qgis, QgsMessageLog

class ProfileBox:
    """ProfileBox represents one layer of a petrographic drilling profile.
    This class contains all relevant data for drawing"""

    def __init__(self, layer):
        """Initialize the box"""
        self.layer = layer
        self.group = self.layer
        self.y = 0.0
        self.width = 0.0
        self.height = 0.0
        self.depth = 0.0
        self.info = ''
        self.color = ''
        self.texture = ''
        self.isFirst = layer == 1
        self.isLast = False

    def paint(self, scene, xpos):
        """Paint box onto scene"""
        pen, brush = self._getPenAndBrush()
        x, y, w, h = self._getPosAndDims(xpos)
        scene.addRect(x, y, w, h, pen, brush)

    def paintDescription(self, scene, xpos):
        """Paint description"""
        width = self._paintDepthMark(scene, xpos)
        if self.isFirst:
            self._paintTopDepthMark(scene, xpos)
        self._paintInfo(scene, xpos, width)

    def _paintTopDepthMark(self, scene, xpos):
        """Paint depth at the top of the layer"""
        x, y, w, h = self._getPosAndDims(xpos)
        d = scene.addText("{:<#5.3n} cm".format(self.depth - self.height))
        d.adjustSize()
        d.setX(x)
        d.setY(y - (d.boundingRect().height() - 2))

        scene.addLine(x, y, x + d.boundingRect().width(), y)

    def _paintDepthMark(self, scene, xpos):
        """Paint depth at the bottom of the layer box"""
        x, y, w, h = self._getPosAndDims(xpos)
        d = scene.addText("{:<#5.3n} cm".format(self.depth))
        d.adjustSize()
        d.setX(x)
        d.setY(y + h - (d.boundingRect().height() - 2))

        scene.addLine(x, y + h, x + d.boundingRect().width(), y + h)
        return d.boundingRect().width()

    def _paintInfo(self, scene, xpos, xoffset):
        """Paint the info text"""
        x, y, w, h = self._getPosAndDims(xpos)
        t = scene.addText(self.info)
        t.setX(x + xoffset)
        t.setY(y)
        t.setTextWidth(200)

    def _getPosAndDims(self, xpos):
        """Scales the position (x, y) as well as width and height"""
        # convert dimensions from cm to mm
        x = xpos * 10
        y = self.y * -10 # direction of y-axis is top down, point (0,0) is in the upper left
        w = self.width * 10
        h = self.height * 10
        return x, y, w, h

    def _getPenAndBrush(self):
        """Get the pen and brush"""
        col = QColor(self.color)
        pen = QPen()
        brush = QBrush(col)
        return pen, brush
