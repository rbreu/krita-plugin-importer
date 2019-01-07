import krita

from .plugin_importer_extension import PluginImporterExtension


krita_instance = krita.Krita.instance()
krita_instance.addExtension(PluginImporterExtension(krita_instance))
