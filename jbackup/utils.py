# Utility functions.

import glob, os

def list_dirs(root: str, *, sanitize=True):
    """
    Returns a list of directories under ROOT.

    ROOT should be a string with the absolute path
    to the directory under which the search should be made.
    """
    res = []

    assert isinstance(root, str), "root not a string"

    for x in glob.glob('*/', root_dir=root):
        if sanitize and x.startswith('_'): continue
        res.append(x.removesuffix('/'))

    return res
