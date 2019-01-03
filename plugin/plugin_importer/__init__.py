try:
    import krita
except ImportError:
    # Unit tests
    pass
else:
    from .plugin_importer_extension import *
