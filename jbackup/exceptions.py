from __future__ import annotations
from typing import Type
from .types import StrPath
import errno

class DirectoryNotFoundError(OSError): # pragma: no cover
    """
    A directory was not found.
    """

    def __init__(self, directory: str | StrPath, *args, **kw):
        super().__init__(*args, **kw)
        self._directory = str(directory)

    def __str__(self) -> str:
        return self.directory

    @property
    def directory(self) -> str:
        "The directory."
        return self._directory

class EnvError(LookupError): # pragma: no cover
    """
    Error for undefined environment variables.
    """

class LoadError(Exception): # pragma: no cover
    """
    Error from loading something.
    """

    def __init__(self, thing: str, msg: str="", /):
        self._thing = thing
        self._msg = msg

    def __str__(self) -> str:
        if self._msg:
            #return "'%s', %s" % (self._thing, self._msg)
            return f"'{self._thing}', {self._msg}"
        return f"'{self._thing}'"

# Warnings

class DebugWarning(Warning): # pragma: no cover
    """
    Warning for debug-only code.
    """

# Factory to create OSError exceptions

class OSErrorFactory: # pragma: no cover
    """
    Singleton that constructs OSError-derived exceptions.

    Each static method constructs an exception with the
    appropriate arguments.
    """

    @staticmethod
    def FileNotFoundError(file1, file2=None):
        """
        Construct a FileNotFoundError.

        FILE1 is the name of the file that caused the exception
        (i.e., the filename passed to the calling function). If
        FILE2 is provided, it represents the second filename passed
        to the calling function (for example, os.rename()).
        """
        file1 = str(file1)
        if file2 is not None:
            return FileNotFoundError(errno.ENOENT, errno.errorcode[errno.ENOENT],
                                     file1, str(file2))
        return FileNotFoundError(errno.ENOENT, errno.errorcode[errno.ENOENT], file1)

def raise_file_not_found_error(file1, file2=None): # pragma: no cover
    """
    Raise FileNotFoundError.
    """
    raise OSErrorFactory.FileNotFoundError(file1, file2)
