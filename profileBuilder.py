"""Module to construct profiles"""

import re
from qgis.core import Qgis, QgsExpression, QgsFeatureRequest, QgsProject, QgsMessageLog

from .geoCoreConfig import Config

class ProfileBuilder:
    """This class constructs the drilling profiles"""

    def __init__(self, showMessage):
        """Features are the 'Stammdaten', i.e. data regarding the drilling profiles.
        config is the configuration element containing metadata to profiles."""
        self.showMessage = showMessage
        self.petroPattern = re.compile(r"(\w+)\s*(\(.*\))?", re.IGNORECASE)
        self.config = Config(self.showErrorMessage)

    def _getSchichtdaten(self, profileId):
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

    def _getLayerAttributes(self, schichtdaten):
        """Get a list of dictionaries containing the layers' attributes"""
        result = []
        for sd in schichtdaten:
            result.append({field.name(): attr for field, attr in zip(sd.fields(), sd.attributes())})
        return result

    def _splitPetrographie(self, petro):
        """Split the given Petrograhie into Großgruppe and Kleingruppe"""
        m = self.petroPattern.match(petro)
        gg = m.group(1) # Großgruppe
        kg = []
        k = m.group(2) # Kleingruppe
        if k is not None:
            # chop off parantheses
            k = k[1:-1]
            # and make a list of it
            k = k.split(",")
            for s in k:
                if not (s.isspace() or (s == '')):
                    kg.append(s)
        return (gg, kg)

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
        profileId = feature.attribute("id")
        schichtdaten = self._getSchichtdaten(profileId)
        if schichtdaten is None:
            return None

        boxes = self.config.geoCore['boxes']
        layerAttributes = self._getLayerAttributes(schichtdaten)
        for l in layerAttributes:
            gg, kg = self._splitPetrographie(l['petrographie'])
            height = l['tiefe bis']-l['tiefe von']
            width = boxes[gg]['width']
            QgsMessageLog.logMessage("Profile {} - petro: {}({}), width: {}, height: {}".format(profileId, gg, kg, width, height), level=Qgis.Info)

        return True

    def _connectProfiles(self, profiles, features):
        """Multiple profiles need to be connected in the drawing"""
        if len(profiles) <= 1:
            return
        pass

    def showErrorMessage(self, title, message):
        """Display an error message"""
        self.showMessage(title, message, Qgis.Critical)
