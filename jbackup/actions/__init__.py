# Actions

from pathlib import Path
from ..utils import list_dirs

def list_actions(root: Path) -> list:
    return list_dirs(
        str(root / 'rules'))
