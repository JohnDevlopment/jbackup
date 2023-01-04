"""Utility functions and classes."""

from __future__ import annotations
from typing import Protocol, Any, cast, Generic, TypeVar, Optional
import glob

T = TypeVar('T')

class DataDescriptor(Generic[T]):
    """Generic data descriptor."""

    def __init__(self, value: T, *, doc: Optional[str]=None):
        self.init_value = value
        if doc:
            self.__doc__ = f"{doc} (default: {value!r})"

    def __get__(self, obj, objtype=None) -> T:
        return obj._value

    def __set__(self, obj, value: T) -> None:
        obj._value = value

class LoadError(Exception):
    """Error from loading something."""

    def __init__(self, thing: str, msg: str="", /):
        self._thing = thing
        self._msg = msg

    def __str__(self) -> str:
        if self._msg:
            return "'%s', %s" % (self._thing, self._msg)
        return "'%s'" % self._thing

class BufferedReadFileDescriptor(Protocol):
    """Protocol for an input file descriptor."""

    def read(self, amt: int=-1) -> bytes:
        ...

class Nil: # pragma: no cover
    """A special value that represents a failure code."""

    def __repr__(self) -> str:
        return "Nil()"

    def __str__(self) -> str:
        return "Nil"

def list_dirs(root: str, *, sanitize=True):
    """
    Returns a list of directories under ROOT.

    ROOT should be a string with the absolute path
    to the directory under which the search should be made.
    """
    res = []

    if not isinstance(root, str):
        raise TypeError(f"invalid root '{root}': not a string")

    for x in glob.glob('*/', root_dir=root):
        if sanitize and x.startswith('_'): continue
        res.append(x.removesuffix('/'))

    return res

class XDictContainer:
    """An extended dictionary."""

    def __init__(self, adict: dict[str, Any], /):
        self._data = adict

    def get(self, key: str, default: Any=None, /) -> Any:
        """
        Returns the value associated with KEY.

        KEY can either be a path-string, with keys
        and subkeys separated by slashes, or a normal
        mapping key, as you see with dict.

        In the former case, KEY is a forward
        slash-separated string denoting a path to the
        value in the underlying dictionary.
        Its syntax is ``key/subkey1[/subkey2...]``.
        This method searches recursively inside the dictionary
        for KEY until it finds a match.

        If there is no value associated with KEY, DEFAULT
        is returned.
        """
        if '/' not in key:
            return self._data.get(key, default)

        return self._get_subkey(self._data, key, default)

    @staticmethod
    def _get_subkey(dct: dict[str, Any], key: str, default: Any, /) -> Any:
        # Call this if KEY has '/' in it.
        # Returns None if no match
        assert key
        assert (lpath := key.split('/'))

        END = len(lpath) - 1
        res = default

        for i, key in enumerate(lpath):
            val = dct.get(key)
            if i == END and val is not None:
                res = val
            elif not isinstance(val, dict):
                break
            dct = cast(dict, val)

        return res

    def __getitem__(self, key: str, /) -> Any:
        """
        Returns the value associated with KEY.

        If no match is found, KeyError is raised.
        """
        if '/' not in key:
            return self._data[key]

        # Get section for toplevel section, or SECTION
        nil = Nil()
        value = self._get_subkey(self._data, key, nil)
        if value is nil:
            raise KeyError(f"'{key}' {value}")

        return value

    def __str__(self) -> str: # pragma: no cover
        return str(self._data)
