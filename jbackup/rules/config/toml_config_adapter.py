"""
Module for reading TOML files.

Functions:
    * read_toml_file()
    * read_toml_string()

Important note about TOML: The result from either of
the read_toml_* functions is a dictionary that maps
a string to an arbitary value. That value, X, will be
a string, number, bool, or a subdictionary depending
on the original value in source.

In TOML, numbers can be integers or floating points.
Boolean values are translated to their Python couter-
parts. Dotted keys are known as tables: 'data.one'
and 'data.two' would result in a subdictionary with
with the 'one' and 'two' keys defined under 'data'.

See read_toml_file() for an example of what such a
dictionary looks like.
"""

from ...utils import BufferedReadFileDescriptor, XDictContainer, Nil
from . import RuleParserError, MissingSectionError, MissingOptionError

try: # pragma: no cover
    import tomllib # type: ignore
    from tomllib import TOMLDecodeError # type: ignore
except:
    import tomli as tomllib # type: ignore
    from tomli import TOMLDecodeError

from typing import Optional, Any, cast

class TOMLFile:
    """TOML config file."""

    def __init__(self, filename: str | BufferedReadFileDescriptor):
        self._data = XDictContainer(self.parse_file(filename))

    @staticmethod
    def parse_file(fileobj_or_string: str | BufferedReadFileDescriptor) -> dict[str, Any]:
        """
        Parse a file and return a dictionary.

        FILEOBJ_OR_STRING can be either a string specifying
        the path to a file or a file descriptor-like object
        containing a read() method.
        """
        data = {}
        err = ""

        try:
            if isinstance(fileobj_or_string, str):
                with open(fileobj_or_string, 'rb') as fd:
                    data = tomllib.load(fd)
            else:
                data = tomllib.load(
                    cast(Any, fileobj_or_string))
        except TOMLDecodeError as exc:
            err = str(exc)

        if err:
            raise RuleParserError(err)

        return data

    def __contains__(self, key: str, /) -> bool:
        nil = Nil()
        if self.get(key, nil) is nil:
            return False
        return True

    def get(self, key: str, default=None) -> Any:
        """
        Return the value associated with KEY.

        The key must contain at least one forward
        slash, or the results might be unexpected.

        KEY is split into two segments, the section
        and the option. The section is the substring
        that occurs before the first forward slash.
        If KEY starts with a slash, the section
        refers to the global section. The option
        refers to the rest of KEY, a forward slash-
        separated list of tags denoting the path
        to a specific value.

        >>> tomlf.get('/config_path') # 'config_path' in global section
        >>> tomlf.get('options/a') # 'a' in section 'options'
        >>> tomlf.get('options/suboptions/a') # 'suboptions/a' in section 'options'

        If the section does not exist, MissingSectionError
        is raised. If the option does not exist,
        MissingOptionError is raised.
        """
        assert '/' in key

        nil = Nil()
        section, _, opt = key.partition('/')

        # Check if the section exists
        if section and self._data.get(section, nil) is nil:
            raise MissingSectionError(f"'{section}'")

        if section:
            section = f"section '{section}'"
        else:
            section = 'global section'
            key = opt

        # Retrieve option under section

        val = self._data.get(key, nil)
        if val is nil:
            raise MissingOptionError(f"'{opt}' in {section}")

        return val
