import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable


@contextmanager
def temporary_file() -> Iterable[Path]:
    _, path = tempfile.mkstemp()
    yield Path(path)
    os.unlink(path)