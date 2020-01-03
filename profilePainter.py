"""This module contains the class profile Painter"""

class ProfilePainter:
    """This class is used to construct the graphics items"""

    def __init__(self, scene):
        """Initialize ProfilePainter.
        All constructed items are added to the scene."""
        self.scene = scene

    def paint(self, otbps, description):
        """Construct items.
        The parameter otbps stands for objects to be painted
        (i.e. profiles and connectors). Parameter description
        denotes if a description shall be added."""
        for i in otbps:
            i.paint(self.scene)
            if description:
                i.paintDescription(self.scene)
