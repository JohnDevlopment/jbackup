"""Load scripts dynamically."""

import types
from typing import Protocol, cast, overload
from importlib.util import spec_from_file_location, module_from_spec
from importlib.machinery import ModuleSpec
from pathlib import Path
from .utils import LoadError, DataDescriptor
import ast

_Module = types.ModuleType

class ModuleLoadError(LoadError):
    """Error while loading an action."""

class _Pathlike(Protocol):
    def __fspath__(self) -> str:
        ...

    def exists(self) -> bool:
        ...

class ModuleProxy:
    """A proxy object for a module."""

    name = DataDescriptor("", doc="The name of the module.")

    def __init__(self, module: _Module, safe: bool, **kw):
        """
        Initialize a proxy for MODULE.

        Creates a module-proxy object for MODULE.
        If SAFE is True, invalid attribute access
        does not raise an exception.

        Keyword arguments:
          * source (str) = a string containing the source
                           code of MODULE. Must be set in order
                           for self.ast_tree to work
        """
        self.__module = module
        self.__safe = safe
        self.__source: str = kw.get('source', '')

    @property
    def ast_tree(self) -> ast.Module:
        """An AST code object representing the module."""
        return ast.parse(self.__source)

    @overload
    def safe(self) -> bool:
        ...

    @overload
    def safe(self, value: bool) -> None:
        ...

    def safe(self, value=None):
        """
        Set or return the 'safe' property.

        If VALUE is not None, 'safe' is set
        to VALUE. Otherwise the value of 'safe'
        is returned.

        Raise TypeError if VALUE is not bool.

        If 'safe' is True, then no exception is
        raised when a nonexistent attribute is
        referenced.
        """
        # Return value if None
        if value is None:
            return self.__safe

        if not isinstance(value, bool):
            raise TypeError(f"invalid value: '{value}', must be a bool")
        self.__safe = value

    def __get(self, key: str):
        res = getattr(self.__module, key)
        if not self.__safe and res is None:
            raise AttributeError(name=key, obj=self)

        return res

    def __getitem__(self, key: str):
        """Implements self[key]."""
        return self.__get(key)

    def __getattr__(self, key: str):
        """Implements self.attr"""
        return self.__get(key)

    def __dir__(self) -> list[str]:
        """Returns the dir of the underlying module."""
        return dir(self.__module)

def load_module_from_file(str_or_path: str | _Pathlike, name: str) -> ModuleProxy:
    """
    Loads a Python script and returns a module with the name NAME.

    If the file does not exist, FileNotFoundError is raised.

    If the module cannot be read from file, ModuleLoadError is raised.
    """
    if isinstance(str_or_path, str):
        str_or_path = Path(str_or_path)

    str_or_path = cast(_Pathlike, str_or_path)

    if not str_or_path.exists():
        raise FileNotFoundError(str(str_or_path))

    # Load spec from file
    spec = spec_from_file_location(name, str(str_or_path))
    if spec is None:
        raise ModuleLoadError("unable to load spec from %s" % str_or_path) # pragma: no cover
    spec = cast(ModuleSpec, spec)

    # Module from spec
    module = module_from_spec(spec)
    assert module is not None

    spec.loader.exec_module(module) # type: ignore

    return ModuleProxy(module, True)

__all__ = [
    # Classes
    'ModuleLoadError',
    'ModuleProxy',

    # Functions
    'load_module_from_file'
]

def main():
    """Main function."""
    import sys
    sysmod = ModuleProxy(sys, False)
    print(dir(sysmod))

if __name__ == "__main__":
    main()
