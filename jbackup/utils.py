"""
Utility functions and classes.
"""

from __future__ import annotations
from collections import namedtuple
from contextlib import contextmanager
from pathlib import Path
from typing import AnyStr, Iterable, Optional, TypeAlias, cast, Type, Any
import itertools
import os
import sys as _sys

from .exceptions import DirectoryNotFoundError, EnvError, OSErrorFactory
from .types import StrPath, T

XDictMapping: TypeAlias = dict[str, Any]

class XDictContainer:
    """
    An extended dictionary.

    Keys are always strings: if a key has slashes (/) in it, it
    is interpreted as a recursive path down the tree. For
    example, the key `section/items` is effectively the same as
    this: `dct['section']['items']`. Without any slashes, the
    key is treated like a normal dictionary key.

    >>> dct = XDictContainer({'section': {'items': [1, 2, 3]}})
    >>> dct['section/items']
    [1, 2, 3]
    """

    class XDictIterator:
        # pylint: disable=missing-class-docstring
        XDictIteratorResult = namedtuple('XDictIteratorResult', ['key', 'value', 'parent'])

        def __init__(self, xdict: XDictContainer):
            self.__obj = xdict
            self._construct()

        def __iter__(self): # pragma: no cover
            return self

        def _construct(self) -> None:
            node = self.__obj.data
            parent = node
            stack: list[tuple[str | int, Any, XDictMapping | list[Any]]] \
                = [(k, v, parent) for k, v in reversed(node.items())]

            self.__stack = stack

        def __next__(self):
            # Return key and value
            stack = self.__stack

            if stack:
                key, node, parent = stack.pop()

                if isinstance(node, dict):
                    node = cast(dict[str, Any], node)
                    stack.extend([(k, v, node) for k, v in reversed(node.items())])
                elif isinstance(node, list):
                    node = cast(list[Any], node)
                    i = len(node) - 1
                    for v in reversed(node):
                        stack.append((i, v, node))
                        i -= 1

                return self.XDictIteratorResult(key, node, parent)

            raise StopIteration

    def __iter__(self):
        return self.XDictIterator(self)

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

        end = len(lpath) - 1
        res = default

        for i, k in enumerate(lpath):
            val = dct.get(k)
            if i == end and val is not None:
                res = val
            elif not isinstance(val, dict):
                break
            dct = cast(dict, val)

        return res

    def __getitem__(self, key: str, /) -> Any:
        if '/' not in key:
            return self._data[key]

        # Get section for toplevel section, or SECTION
        nil = object()
        value = self._get_subkey(self._data, key, nil)
        if value is nil:
            raise KeyError(f"'{key}' {value}")

        return value

    def __str__(self) -> str: # pragma: no cover
        return str(self._data)

    def __repr__(self) -> str:
        return f"XDictContainer({self._data!r})"

    @property
    def data(self) -> dict[str, Any]:
        "The internal data."
        return self._data

def get_env(name: str, default: Optional[T]=None,
            *, type_: Optional[Type[T]]=str) -> T | str:
    """
    Return the environment variable NAME.

    If NAME cannot be obtained, then provided DEFAULT
    is not None, it will be returned. But if DEFAULT
    is None, then EnvError is raised.

    TYPE_ is used to convert the result to a type
    other than str. TypeError is raised if it is not
    a valid type or is None. Such conversions are done
    by passing the the string result into the class
    initializer. list is an exception: the string is
    parsed as a Python expression, with the end result
    being a list object.
    """
    if type_ is None or not isinstance(type_, type):
        raise TypeError("type_ must be a valid type")

    # Get environment variable. If None and
    # and no default, raise error. Else if
    # default provided, use its type
    res = os.getenv(name)
    if res is None:
        if default is None:
            raise EnvError(name)
        type_ = type(default)
        res = default

    # Convert result to a non-string type
    if type_ != str:
        if type_ is list:
            # Convert into a list
            # pylint: disable=eval-used
            res = cast(str, res)
            code = compile(res.replace('true', 'True'),
                           __file__, 'eval')
            return eval(code)

        cls = cast(Type[T], type_)
        return cls(res)

    return cast(str, res)

@contextmanager
def chdir_temp(d: StrPath):
    old_pwd = chdir(d)
    yield Path(d)
    chdir(old_pwd)
    return old_pwd

def chdir(_dir: StrPath) -> Path:
    """
    Change the current working directory.

    The argument is either a string or a Path
    pointing to the directory to switch to.
    TypeError is raised if 

    DirectoryNotFoundError is raised if the
    directory does not exist. NotADirectoryError
    is raised if the directory is in fact not
    a directory.

    The previous working directory is returned.
    """
    # Type check
    t = type(_dir)
    if t is not str and not issubclass(t, Path):
        raise TypeError(f"'{_dir}' is not a string or a path")

    # Convert from a string to a path
    # Expand '~' to the user directory
    if t is str:
        _dir = Path(_dir).expanduser()
    else:
        _dir = cast(Path, _dir).expanduser()

    oldpwd = Path.cwd()

    # Error checks
    e = None
    if not _dir.exists():
        e = DirectoryNotFoundError(_dir)
    elif not _dir.is_dir():
        e = OSErrorFactory.NotADirectoryError(_dir)

    if e is not None:
        raise e

    os.chdir(_dir)

    return oldpwd

def eprintf(fmt: AnyStr, *args: Any):
    print(fmt % args, file=_sys.stderr)

def iter_nonempty(iterable: Iterable[AnyStr]) -> itertools.filterfalse[AnyStr]:
    """
    Return an iterator that filters empty strings from ITERABLE.
    """
    return itertools.filterfalse(lambda x: len(x) == 0 or x.isspace(), iterable)
