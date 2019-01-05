import builtins
import sys
from unittest.mock import MagicMock


sys.modules['krita'] = MagicMock()

builtins.i18n = lambda s: s
