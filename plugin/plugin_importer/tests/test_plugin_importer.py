import os
import pytest
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch


from .. plugin_importer import PluginImporter, PluginReadError


class PluginImporterTestCase(TestCase):

    def setUp(self):
        self.resources_dir = TemporaryDirectory()
        self.plugin_dir = TemporaryDirectory()

    def tearDown(self):
        self.resources_dir.cleanup()
        self.plugin_dir.cleanup()

    @property
    def zip_filename(self):
        return os.path.join(
            self.resources_dir.name, 'plugin.zip')

    @patch('builtins.i18n')
    def test_zipfile_doesnt_exist(self, patcher):
        with pytest.raises(PluginReadError) as excinfo:
            PluginImporter(self.zip_filename,
                           self.resources_dir.name,
                           lambda x: True)
        assert 'No such file' in str(excinfo)

    def test_zipfile_not_a_zip(self):
        with open(self.zip_filename, 'w') as f:
            f.write('foo')
        with pytest.raises(PluginReadError) as excinfo:
            PluginImporter(self.zip_filename,
                           self.resources_dir.name,
                           lambda x: True)
        assert 'not a zip file' in str(excinfo)
