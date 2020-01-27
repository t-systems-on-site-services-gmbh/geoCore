"""Module to construct profiles"""

import re
from math import sqrt
from qgis.core import Qgis, QgsExpression, QgsFeatureRequest, QgsProject, QgsMessageLog
from qgis.PyQt.QtCore import QVariant

from .geoCoreConfig import Config
from .profile import Profile
from .profileBox import ProfileBox
from .connector import Connector

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

        # we may want to sort the features by "schichtnr"
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

    def getProfilesAndConnectors(self, features):
        """Get the drilling profiles and its connectors"""
        profiles = []
        if len(features) > 0:
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
                profiles.append(self._getProfile(f, xp, yp))

        actualProfiles = []
        actualFeatures = []
        for p, f in zip(profiles, features):
            if p is not None:
                actualProfiles.append(p)
                actualFeatures.append(f)
        if len(actualProfiles) == 0:
            self.showMessage("Info", "Select at least one feature or activate the correct layer.", Qgis.Info)

        connectors = self._connectProfiles(actualProfiles, actualFeatures)

        return actualProfiles + connectors

    def _getProfile(self, feature, x, y):
        """Construct a profile from feature"""
        profileId = feature.attribute("id")
        schichtdaten = self._getSchichtdaten(profileId)
        if schichtdaten is None:
            return None

        profile = Profile(profileId)
        profile.x = x
        profile.y = y

        boxes = self.config.geoCore['boxes']
        colors = self.config.geoCore['colors']
        descriptions = self.config.geoCore['descriptions']
        facies = self.config.geoCore['facies']
        layerAttributes = self._getLayerAttributes(schichtdaten)
        for l in layerAttributes:
            pb = ProfileBox(l['schichtnr'])
            pb.group = l['gruppierung']
            pb.isLast = l['schichtnr'] == len(layerAttributes)
            pb.y = y
            pb.height = l['tiefe bis']-l['tiefe von']
            pb.depth = l['tiefe bis']

            gg, kg = self._splitPetrographie(l['petrographie'])
            pb.width = boxes[gg]['width']

            color = self._cfgLookup(colors, l['farbe'])
            pb.color = self._cfgLookup(color, 'code')
            pb.texture = self._cfgLookup(color, 'texture', showError=False)

            ggDict = self._cfgLookup(boxes, gg)
            infoList = []
            infoList.append(self._cfgLookup(facies, l['facies']))
            infoList.append(self._cfgLookup(ggDict, 'longname'))
            for k in kg:
                kgDict = self._cfgLookup(descriptions, k)
                infoList.append(self._cfgLookup(kgDict, 'longname'))
            infoList.append(l['beschreibung'])
            infoList.append(self._cfgLookup(color, 'longname'))
            pb.info = ", ".join([i for i in infoList if (i is not None) and not isinstance(i, QVariant)])

            profile.boxes.append(pb)

            #QgsMessageLog.logMessage("Profile {} - petro: {}({}), width: {}, height: {}, x: {}, y: {}, info: {}".format(profileId, gg, kg, width, height, x, y, info), level=Qgis.Info)
            y = y - pb.height

        return profile

    def _cfgLookup(self, dictionary, key, showError=True):
        """Return key from dictionary. Return None if key not found."""
        try:
            if (dictionary is not None) and not isinstance(key, QVariant):
                return dictionary[key]
        except KeyError:
            if showError:
                self.showErrorMessage("Error", "Key {} not found in config.".format(key))
        return None

    def _connectProfiles(self, profiles, features):
        """Multiple profiles need to be connected in the drawing"""
        if len(profiles) <= 1:
            return []

        connectors = []

        i = 1 # we start with the second profile connecting it with the first
        minLen = min(len(profiles), len(features))
        while i < minLen:
            cs = self._connectTwoProfiles(profiles[i - 1], profiles[i])
            for c in cs:
                connectors.append(c)
            i = i + 1

        return connectors

    def _connectTwoProfiles(self, pLeft, pRight):
        """Get connectors for left and right profile"""
        connectors = []

        # last group on the left and right
        lgLeft = None

        # y-coordinates
        yLeft = pLeft.y
        yRight = pRight.y

        l = 0
        r = 0
        while l < len(pLeft.boxes):
            if lgLeft != pLeft.boxes[l].group:
                # new connector
                c = Connector()
                c.x1 = pLeft.x + pLeft.boxes[l].width
                c.y1 = yLeft

                # find the corresponding group on the right side
                found = False
                while (r < len(pRight.boxes)) and not found:
                    if pLeft.boxes[l].group == pRight.boxes[r].group:
                        c.x2 = pRight.x
                        c.y2 = yRight
                        found = True
                    yRight = yRight - pRight.boxes[r].height
                    r = r + 1

                connectors.append(c)
            lgLeft = pLeft.boxes[l].group
            yLeft = yLeft - pLeft.boxes[l].height

            if l == len(pLeft.boxes) - 1:
                # last profile box on the left
                c = Connector()
                c.x1 = pLeft.x + pLeft.boxes[l].width
                c.y1 = pLeft.y - pLeft.height()

                # connect to last corresponding group on the right
                rr = len(pRight.boxes) - 1
                while rr >= r - 1:
                    QgsMessageLog.logMessage("groupLeft: {}, groupRight: {}".format(pLeft.boxes[l].group, pRight.boxes[rr].group), level=Qgis.Info)
                    if pLeft.boxes[l].group == pRight.boxes[rr].group:
                        c.x2 = pRight.x
                        c.y2 = pRight.y - pRight.height()
                        QgsMessageLog.logMessage("BREAK Profile.y {}, height: {}, y: {}".format(pRight.y, pRight.height(), c.y2), level=Qgis.Info)
                        break
                    rr = rr - 1

                QgsMessageLog.logMessage("Profile.y {}, height: {}, y: {}".format(pRight.y, pRight.height(), c.y2), level=Qgis.Info)
                connectors.append(c)

            l = l + 1

        return connectors

    def showErrorMessage(self, title, message):
        """Display an error message"""
        self.showMessage(title, message, Qgis.Critical)
