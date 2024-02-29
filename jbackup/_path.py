"""Functions and variables for paths."""

from __future__ import annotations
from pathlib import Path

DATAPATHS = {
    'system': Path('/usr/local/etc/jbackup'),
    'user': Path('~/.local/etc/jbackup').expanduser()
}

def get_data_path() -> Path:
    """Return the data path appropriate to the user."""

    datapath: Path = DATAPATHS['system']

    f = datapath.parent / 'tmpjbackuproottest'
    try:
        with f.open('w') as fd:
            fd.write('...')
        f.unlink()
    except PermissionError:
        datapath = DATAPATHS['user']

    return datapath
