""" Module to construct profiles

    geoCore - a QGIS plugin for drawing drilling profiles
    Copyright (C) 2019 - 2021  Gerrit Bette, T-Systems on site services GmbH

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

import re
from math import sqrt
from sys import maxsize
from qgis.core import Qgis, QgsExpression, QgsFeatureRequest, QgsProject
# from qgis.core import QgsMessageLog
from qgis.PyQt.QtCore import QVariant

from .geoCoreConfig import Config
from .profile import Profile
from .profileBox import ProfileBox
from .connector import Connector
from .orientation import Orientation
from .gauge import Gauge

class ProfileBuilder:
    """This class constructs the drilling profiles"""

    def __init__(self, layerName, showMessage):
        """Features are the 'Stammdaten', i.e. data regarding the drilling profiles.
        config is the configuration element containing metadata to profiles."""
        self.nameLayerSchichtdaten = "{}_data".format(layerName)
        self.showMessage = showMessage
        self.petroPattern = re.compile(r"(\w*)\s*(\(.*\))?", re.IGNORECASE)
        self.config = Config(self.showErrorMessage)

    def _getSchichtdaten(self, profileId):
        """Get the Schichtdaten corresponding to given drilling profile"""
        qex = QgsExpression(QgsExpression().createFieldEqualityExpression(self.config.settings["dataId"], profileId))
        qfr = QgsFeatureRequest(qex)
        layerSchichtdaten = QgsProject().instance().mapLayersByName(self.nameLayerSchichtdaten)

        if len(layerSchichtdaten) == 0:
            self.showErrorMessage("Error", "Layer {} not found.".format(self.nameLayerSchichtdaten))
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
        if not isinstance(petro, str):
            return (None, [])
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
            x = features[0].attribute(self.config.settings["xCoord"])
            y = features[0].attribute(self.config.settings["yCoord"])
            xp = 0
            for f in features:
                # The x-position (xp) of the drilling profile is the distance
                # to the previous coordinate. We start with xp = 0.
                # The y-position of the profile is the elevation (z-coordinate).
                distance = sqrt((f.attribute(self.config.settings["xCoord"]) - x)**2
                            + (f.attribute(self.config.settings["yCoord"]) - y)**2)
                xp = xp + distance
                yp = f.attribute(self.config.settings["zCoord"]) * 100 # convert to cm

                profiles.append(self._getProfile(f.attribute(self.config.settings["boreholeId"]), xp * 100, yp))

                x = f.attribute(self.config.settings["xCoord"])
                y = f.attribute(self.config.settings["yCoord"])

        actualProfiles = []
        actualFeatures = []
        for p, f in zip(profiles, features):
            if p is not None:
                actualProfiles.append(p)
                actualFeatures.append(f)
        if len(actualProfiles) == 0:
            self.showMessage("Info", "Select at least one feature or activate the correct layer.", Qgis.Info)

        connectors = self._connectProfiles(actualProfiles, actualFeatures)
        gauges = self._getGauges(actualProfiles)

        return actualProfiles + connectors + gauges

    def _getProfile(self, profileId, x, y):
        """Construct a profile from feature"""
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
            pb = ProfileBox(l[self.config.settings["layerNo"]])
            pb.group = l[self.config.settings["group"]]
            pb.isLast = l[self.config.settings["layerNo"]] == len(layerAttributes)
            pb.y = y
            pb.height = l[self.config.settings["depthTo"]]-l[self.config.settings["depthFrom"]]
            pb.depth = l[self.config.settings["depthTo"]]

            gg, kg = self._splitPetrographie(l[self.config.settings["petrography"]])
            pb.name = gg
            try:
                pb.width = boxes[gg]['width']
            except KeyError:
                pb.width = 0.1
                self.showMessage("Warning", "Missing main group in petrography: {}"
                    .format(l[self.config.settings["petrography"]]), Qgis.Warning)

            color = self._cfgLookup(colors, l[self.config.settings["color"]])
            pb.color = self._cfgLookup(color, 'code')
            pb.texture = self._cfgLookup(color, 'texture', showError=False)

            ggDict = self._cfgLookup(boxes, gg)
            infoList = []
            infoList.append(self._cfgLookup(facies, l[self.config.settings["facies"]],
                errorValue=l[self.config.settings["facies"]]))
            infoList.append(self._cfgLookup(ggDict, 'longname', errorValue=gg))
            for k in kg:
                kgDict = self._cfgLookup(descriptions, k)
                infoList.append(self._cfgLookup(kgDict, 'longname', errorValue=k))
            infoList.append(l[self.config.settings["comment"]])
            infoList.append(self._cfgLookup(color, 'longname'))
            pb.info = ", ".join([i for i in infoList if (i is not None) and not isinstance(i, QVariant)])

            profile.boxes.append(pb)

            # QgsMessageLog.logMessage("Profile {} - petro: {}({}), width: {}, height: {}, x: {}, y: {}, info: {}"
            #     .format(profileId, gg, kg, pb.width, pb.height, x, y, pb.info), level=Qgis.Info)
            y = y - pb.height

        return profile

    def _cfgLookup(self, dictionary, key, showError=True, errorValue=None):
        """Return key from dictionary. Return None if key not found."""
        try:
            if (dictionary is not None) and not isinstance(key, QVariant):
                return dictionary[key]
        except KeyError:
            if showError:
                self.showMessage("Info", "Key {} not found in config.".format(key), Qgis.Info)
        return errorValue

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
                c.x1 = pLeft.x
                c.y1 = yLeft
                c.xOffset = pLeft.boxes[l].width

                # find the corresponding group on the right side
                found = False
                while (r < len(pRight.boxes)) and not found:
                    if pLeft.boxes[l].group == pRight.boxes[r].group:
                        c.x2 = pRight.x
                        c.y2 = yRight
                        found = True
                        connectors.append(c)
                    yRight = yRight - pRight.boxes[r].height
                    r = r + 1

            lgLeft = pLeft.boxes[l].group
            yLeft = yLeft - pLeft.boxes[l].height

            if len(pLeft.boxes) != len(pRight.boxes) and r == len(pRight.boxes):
                # last profile box on the right but not on the left
                c = Connector()
                c.x2 = pRight.x
                c.y2 = pRight.y - pRight.height()

                found = False
                ll = len(pLeft.boxes) - 1
                while ll >= l and not found:
                    if pLeft.boxes[ll].group == pRight.boxes[r - 1].group:
                        c.x1 = pLeft.x
                        c.y1 = pLeft.y - sum([b.height for b in pLeft.boxes[:ll+1]])
                        c.xOffset = pLeft.boxes[ll].width
                        found = True
                        connectors.append(c)
                    ll = ll - 1

            if l == len(pLeft.boxes) - 1:
                # last profile box on the left
                c = Connector()
                c.x1 = pLeft.x
                c.y1 = pLeft.y - pLeft.height()
                c.xOffset = pLeft.boxes[l].width

                # connect to last corresponding group on the right
                found = False
                rr = len(pRight.boxes) - 1
                while (rr >= r - 1) and not found:
                    if pLeft.boxes[l].group == pRight.boxes[rr].group:
                        c.x2 = pRight.x
                        c.y2 = pRight.y - sum([b.height for b in pRight.boxes[:rr+1]])
                        found = True
                        connectors.append(c)
                    rr = rr - 1

            l = l + 1

        return connectors

    def _getGauges(self, profiles):
        """Gets the gauges for the left and bottom side"""
        if len(profiles) <= 1:
            return []

        minx, maxx, miny, maxy = self._determineMinMax(profiles)

        gauges = []
        gauges.append(Gauge(minx, miny, minx, maxx, Orientation.HORIZONTAL))
        gauges.append(Gauge(minx, miny, miny, maxy, Orientation.VERTICAL))

        return gauges

    def _determineMinMax(self, profiles):
        """Determine the min and max values in x- and y-dimension"""
        minx = maxsize
        maxx = 0
        miny = maxsize
        maxy = 0
        for p in profiles:
            minx = min(minx, p.x)
            maxx = max(maxx, p.x)
            miny = min(miny, p.y, p.y - p.height())
            maxy = max(maxy, p.y, p.y - p.height())
        return minx, maxx, miny, maxy

    def showErrorMessage(self, title, message):
        """Display an error message"""
        self.showMessage(title, message, Qgis.Critical)
