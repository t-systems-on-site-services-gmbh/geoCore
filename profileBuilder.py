"""Module to construct profiles"""

import re
from math import sqrt
from qgis.core import Qgis, QgsExpression, QgsFeatureRequest, QgsProject, QgsMessageLog
from qgis.PyQt.QtCore import QVariant

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
            kg = [s.strip() for s in k.split(",") if not (s.isspace() or (s == ''))]
        return (gg, kg)

    def drawProfiles(self, features, showInfo):
        """Construct the drilling profiles
        Parameter showInfo denotes if the drawing shall
        contain textual information about the layers."""
        profiles = []
        x = features[0].attribute('xcoord')
        y = features[0].attribute('ycoord')
        for f in features:
            # The x-position (xp) of the drilling profile is the distance
            # to the previous coordinate. We start with xp = 0.
            # The y-position of the profile is the elevation (z-coordinate).
            xp = sqrt((f.attribute('xcoord') - x)**2 + (f.attribute('ycoord') - y)**2)
            yp = f.attribute('zcoorddb') * 100 # convert to cm
            x = f.attribute('xcoord')
            y = f.attribute('ycoord')
            profiles.append(self._drawProfile(f, xp, yp, showInfo))

        actualProfiles = []
        actualFeatures = []
        for p, f in zip(profiles, features):
            if p is not None:
                actualProfiles.append(p)
                actualFeatures.append(f)
        if len(actualProfiles) == 0:
            self.showMessage("Info", "Select at least one feature or activate the correct layer.", Qgis.Info)

        self._connectProfiles(actualProfiles, actualFeatures)

    def _drawProfile(self, feature, x, y, showInfo):
        """Construct a profile from feature"""
        profileId = feature.attribute("id")
        schichtdaten = self._getSchichtdaten(profileId)
        if schichtdaten is None:
            return None

        boxes = self.config.geoCore['boxes']
        colors = self.config.geoCore['colors']
        descriptions = self.config.geoCore['descriptions']
        facies = self.config.geoCore['facies']
        layerAttributes = self._getLayerAttributes(schichtdaten)
        for l in layerAttributes:
            isFirst = l['schichtnr'] == 1
            isLast = l['schichtnr'] == len(layerAttributes)
            gg, kg = self._splitPetrographie(l['petrographie'])
            height = l['tiefe bis']-l['tiefe von']
            width = boxes[gg]['width']
            color = self._cfgLookup(colors, l['farbe'])
            info = ""
            if showInfo:
                ggDict = self._cfgLookup(boxes, gg)
                infoList = []
                infoList.append(self._cfgLookup(facies, l['facies']))
                infoList.append(self._cfgLookup(ggDict, 'longname'))
                for k in kg:
                    kgDict = self._cfgLookup(descriptions, k)
                    infoList.append(self._cfgLookup(kgDict, 'longname'))
                infoList.append(l['beschreibung'])
                infoList.append(self._cfgLookup(color, 'longname'))
                info = ", ".join([i for i in infoList if (i is not None) and not isinstance(i, QVariant)])             
            
            #QgsMessageLog.logMessage("Profile {} - petro: {}({}), width: {}, height: {}, x: {}, y: {}, info: {}".format(profileId, gg, kg, width, height, x, y, info), level=Qgis.Info)
            y = y - height

        return True

    def _cfgLookup(self, dictionary, key):
        """Return key from dictionary. Return None if key not found."""
        try:
            if (dictionary is not None) and not isinstance(key, QVariant):
                return dictionary[key]
        except KeyError:
            self.showErrorMessage("Error", "Key {} not found in config.".format(key))
        return None

    def _connectProfiles(self, profiles, features):
        """Multiple profiles need to be connected in the drawing"""
        if len(profiles) <= 1:
            return
        pass

    def showErrorMessage(self, title, message):
        """Display an error message"""
        self.showMessage(title, message, Qgis.Critical)
