"""Dialog to configure profile box captions"""

import os

from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtCore import Qt

from .profileBuilder import ProfileBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), "caption_dialog_base.ui"))


class CaptionDialog(QtWidgets.QDialog, FORM_CLASS):
    """Dialog for configuring the content and order of profile box captions."""

    LABELS = {
        "facies": "Facies",
        "mainGroup": "Main petrographic group",
        "subgroups": "Petrographic subgroups",
        "comment": "Comment",
        "color": "Color",
    }

    def __init__(self, order, enabled, parent=None):
        """Constructor."""
        super(CaptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.fields.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.fields.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.defaultsButton.clicked.connect(self._restoreDefaults)
        self._populate(order, enabled)

    def _populate(self, order, enabled):
        """Show every field, preserving disabled fields' positions."""
        self.fields.clear()
        for field in order:
            item = QtWidgets.QListWidgetItem(self.LABELS[field], self.fields)
            item.setData(Qt.ItemDataRole.UserRole, field)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsDragEnabled)
            item.setCheckState(Qt.CheckState.Checked if field in enabled else Qt.CheckState.Unchecked)

    def _restoreDefaults(self):
        """Restore the original caption contents and ordering in the dialog."""
        fields = ProfileBuilder.CAPTION_FIELDS
        self._populate(fields, fields)

    def captionOrder(self):
        """Return all field identifiers in their current order."""
        return [self.fields.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.fields.count())]

    def captionEnabled(self):
        """Return enabled identifiers, ordered as displayed."""
        return [
            self.fields.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.fields.count())
            if self.fields.item(i).checkState() == Qt.CheckState.Checked
        ]
