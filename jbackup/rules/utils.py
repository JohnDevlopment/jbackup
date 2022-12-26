"""
Utilities specific to rules.

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

try:
    import tomllib # type: ignore
    from tomllib import TOMLDecodeError # type: ignore
except:
    import tomli as tomllib # type: ignore
    from tomli import TOMLDecodeError

from typing import Optional, Any

def read_toml_file(filename: str) -> dict[str, Any]:
    """
    Loads FILENAME and parses its contents as TOML, 
    returning a dictionary.

    Each section in the TOML code corresponds to
    a key in the dictionary.

    If the attempt to parse the TOML data fails,
    TOMLDecodeError is raised.

    Internally, open() is called, so OSError will be
    raised if the attempt at opening FILENAME fails.

    file.toml:

      [section]
      table.number = 1
      table.boolean = true
      string = "adjlvsdjl"

    >>> data = read_toml_file('file.toml')
    >>> print(repr(data))
    {'section': {'table': {'number': 1, 'boolean': True}, 'string': 'adjlvsdjl'}}
    """
    with open(filename, 'rb') as fd:
        data = tomllib.load(fd)

    return data

def read_toml_string(data: str) -> dict[str, Any]:
    """
    Reads DATA as a TOML string and returns a dictionary.

    The dictionary has the same structure as it would
    being returned from read_toml_file(), so see that
    for more details.

    If the attempt to parse the TOML data fails,
    TOMLDecodeError is raised.
    """
    return tomllib.loads(data)

__all__ = [
    # Functions
    'read_toml_file',
    'read_toml_string',

    # Classes
    'TOMLDecodeError'
]
