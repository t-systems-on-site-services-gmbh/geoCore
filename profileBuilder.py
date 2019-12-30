"""Module to construct profiles"""

from qgis.core import Qgis, QgsExpression, QgsFeatureRequest, QgsProject

from .geoCoreConfig import Config

class ProfileBuilder:
    """This class constructs the drilling profiles"""

    def __init__(self, showMessage):
        """Features are the 'Stammdaten', i.e. data regarding the drilling profiles.
        config is the configuration element containing metadata to profiles."""
        self.showMessage = showMessage
        self.config = Config(self.showErrorMessage)

    def isFeatureAdmissible(self, feature):
        """Checks if feature is admissible,
        i.e. do we have "Schichtdaten" for it."""
        profileId = feature.attribute("id")
        return self.getSchichtdaten(profileId) is not None

    def getSchichtdaten(self, profileId):
        """Get the Schichtdaten corresponding to given drilling profile"""
        # As of now we need to chop off the leading letter.
        # This might change in the future.
        qex = QgsExpression(QgsExpression().createFieldEqualityExpression("ID", profileId[1:]))
        qfr = QgsFeatureRequest(qex)
        layerSchichtdaten = QgsProject().instance().mapLayersByName(self.config.settings["layerSchichtdaten"])

        if len(layerSchichtdaten) == 0:
            self.showErrorMessage("Error", "Layer {} not found.".format(self.config.settings["layerSchichtdaten"]))
            return None

        return layerSchichtdaten[0].getFeatures(qfr)

    def drawProfiles(self, features):
        """Construct the drilling profiles"""
        profiles = [self._drawProfile(f) for f in features]
        
        actualProfiles = []
        actualFeatures = []
        for p, f in zip(profiles, features):
            if p is not None:
                actualProfiles.append(p)
                actualFeatures.append(f)
        if len(actualProfiles) == 0:
            self.showMessage("Info", "Select at least one feature or activate the correct layer.", Qgis.Info)

        self._connectProfiles(actualProfiles, actualFeatures)

    def _drawProfile(self, feature):
        """Construct a profile from feature"""
        if self.isFeatureAdmissible(feature):
            return None
        return True

    def _connectProfiles(self, profiles, features):
        """Multiple profiles need to be connected in the drawing"""
        if len(profiles) <= 1:
            return
        pass

    def showErrorMessage(self, title, message):
        """Display an error message"""
        self.showMessage(title, message, Qgis.Critical)
