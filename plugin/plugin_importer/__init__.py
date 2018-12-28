import os

import krita
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from .plugin_importer import PluginImporter


class PluginImportertExtension(krita.Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(
            'plugin_importer',
            'Import Python Plugin...',
            'tools/scripts')
        action.triggered.connect(self.import_plugin)

    def confirm_overwrite(self, plugin):
        reply =  QMessageBox.question(
            self.parent.activeWindow().qwindow(),
            'Overwrite Plugin',
            'The plugin "%s" already exists. Overwrite it?' % (
                plugin['ui_name']),
            QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_success_text(self, plugins):
        txt = [
            '<p>The following plugins were imported:</p>',
            '<ul>'
        ]
        for plugin in plugins:
            txt.append('<li>%s</li>' % plugin['ui_name'])

        txt.append('</ul>')
        txt.append(
            '<p>Please restart Krita and activate the plugins in '
            '<em>Settings -> Configure Krita -> '
            'Python Plugin Manager</em>.</p>')
        return ('\n').join(txt)

    def import_plugin(self):
        zipfile = QFileDialog.getOpenFileName(
            self.parent.activeWindow().qwindow(),
            'Import Plugin',
            os.path.expanduser('~'),
            'Zip Archives (*.zip)'
        )[0]
        resources_dir = os.path.expanduser('~/.local/share/krita')

        imported = PluginImporter(
            zipfile, resources_dir, self.confirm_overwrite
        ).import_all()

        if imported:
            QMessageBox.information(
                self.parent.activeWindow().qwindow(),
                'Import successful',
                self.get_success_text(imported))


krita_instance = krita.Krita.instance()
krita_instance.addExtension(PluginImportertExtension(krita_instance))
