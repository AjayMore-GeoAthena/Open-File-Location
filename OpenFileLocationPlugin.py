import os
import sys
import subprocess
from qgis.PyQt.QtWidgets import QAction, QMessageBox

class OpenFileLocationPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.layer_tree_view = None
        self.action = None

    def initGui(self):
        self.layer_tree_view = self.iface.layerTreeView()

        # Create the action
        self.action = QAction("Open File Location", self.iface.mainWindow())
        self.action.triggered.connect(self.open_location)

        # QGIS 3.34 signal: ONLY ONE ARGUMENT
        self.layer_tree_view.contextMenuAboutToShow.connect(self.add_to_menu)

    def unload(self):
        try:
            self.layer_tree_view.contextMenuAboutToShow.disconnect(self.add_to_menu)
        except Exception:
            pass

    def add_to_menu(self, menu):
        """Called every time the user right-clicks in the layer tree."""
        node = self.layer_tree_view.currentNode()
        if not node:
            return

        layer = node.layer()
        if not layer:
            return

        source = layer.source().split("|")[0]
        if not os.path.exists(source):
            return  # Only show for file-based layers

        menu.addAction(self.action)

    def open_location(self):
        layer = self.iface.activeLayer()
        if not layer:
            QMessageBox.warning(None, "No Layer Selected", "Please select a layer.")
            return

        source = layer.source().split("|")[0]

        if not os.path.exists(source):
            QMessageBox.warning(None, "Invalid Source", f"Cannot locate file:\n{layer.source()}")
            return

        folder = source if os.path.isdir(source) else os.path.dirname(source)

        if os.name == "nt":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])