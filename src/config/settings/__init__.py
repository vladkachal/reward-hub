import contextlib

from .base import *  # noqa

with contextlib.suppress(ImportError):
    from .local import *  # noqa
