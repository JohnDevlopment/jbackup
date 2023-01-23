"""Utility functions and classes."""

from __future__ import annotations
from typing import Protocol, Any, cast, Generic, TypeVar, Optional, Type
import glob, os

T = TypeVar('T')

__all__ = [
    # Classes
    'BufferedReadFileDescriptor',
    'ConstantError',
    'DataDescriptor',
    'DirectoryNotEmptyError',
    'DirectoryNotFoundError',
    'EnvError',
    'LoadError',
    'Nil',
    'Pathlike',
    'XDictContainer',

    # Functions
    'get_env',
    'list_dirs'
]

class DataDescriptor(Generic[T]):
    """Generic data descriptor."""

    def __init__(self, value: T, *, doc: Optional[str]=None, frozen: bool=False):
        self._init = False
        self.frozen: bool = frozen
        self._value: T = value
        if doc:
            if frozen:
                doc += "\n\nThis is a readonly variable. " + \
                    f"(Value: {value!r})"
            else:
                doc += f"\n\nThe default value is {value!r}."
            self.__doc__ = doc

    def __set_name__(self, owner: type, name: str):
        assert isinstance(name, str)
        assert isinstance(owner, type)
        self.name: str = name
        self.owner: type = owner
        self.private_name = '_' + self.name

    def __get__(self, obj, _objtype=None) -> T:
        return getattr(obj, self.private_name)

    def __set__(self, obj, value: T) -> None:
        # Already set once before
        if self.frozen and self._init:
            raise ConstantError(self.name, owner=self.owner)
        setattr(obj, self.private_name, value)
        self._init = True

class Pathlike(Protocol):
    def __fspath__(self) -> str:
        """Called by os.fspath()."""
        ...

    def exists(self) -> bool:
        """Whether path exists."""
        ...

    def is_absolute(self) -> bool:
        """Where iath is an absolute one."""
        ...

    def __str__(self) -> str:
        ...

class DirectoryNotFoundError(OSError):
    """A directory was not found."""

    directory = DataDescriptor("", doc="The directory.", frozen=True)

    def __init__(self, directory: str | Pathlike, *args, **kw):
        super().__init__(*args, **kw)
        self.directory = str(directory)

    def __str__(self) -> str:
        return self.directory

class DirectoryNotEmptyError(OSError):
    """The directory is not empty."""

    files = DataDescriptor([""], doc="List of files.", frozen=True)
    directory = DataDescriptor("", doc="The directory.")

    def __init__(self, directory: str, *args, **kw):
        self.directory = directory
        self.files = [str(f) for f in kw.pop('files', [])]
        super().__init__(*args, **kw)

    def __str__(self) -> str:
        return self.directory

class ConstantError(Exception):
    def __init__(self, name: str, *, owner=None):
        self.msg = f"cannot reassign to frozen attribute '{name}'"
        self.owner = owner

    def __str__(self) -> str:
        msg = self.msg
        if self.owner:
            msg += f" (owned by {self.owner})"
        return msg

class EnvError(LookupError):
    """Error for undefined environment variables."""

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
            res = cast(str, res)
            code = compile(res.replace('true', 'True'),
                           __file__, 'eval')
            return eval(code)

        cls = cast(Type[T], type_)
        return cls(res)

    return cast(str, res)

def list_dirs(root: str, *, sanitize=True) -> list[str]:
    """
    Returns a list of directories under ROOT.

    ROOT should be a string with the absolute path
    to the directory under which the search should be made.
    """
    res: list[str] = []

    if not isinstance(root, str):
        raise TypeError(f"invalid root '{root}': not a string")

    for x in glob.glob('*/', root_dir=root):
        if sanitize and x.startswith('_'): continue
        res.append(x.removesuffix('/'))

    return res
