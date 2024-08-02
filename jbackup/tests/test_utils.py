from __future__ import annotations
from pathlib import Path
from typing import Any, TypeAlias, TypeVar
from ..utils import DirectoryNotFoundError, EnvError, XDictContainer, chdir, get_env

import pytest

T = TypeVar('T')

StrDict: TypeAlias = dict[str, T]

def test_get_env():
    value = get_env("TEST_STRING")
    assert isinstance(value, str)

    value = get_env("TEST_INT", type_=int)
    assert isinstance(value, int)

    value = get_env("TEST_LIST", type_=list)
    assert isinstance(value, list)

    with pytest.raises(TypeError):
        get_env("TEST_INT", type_=1) # type: ignore

    with pytest.raises(EnvError):
        get_env("INVALID")

def test_chdir(tmp_path: Path):
    d = tmp_path / "subdir"
    d.mkdir()

    # Using a string argument
    oldpwd = chdir(str(d))

    # Using a path argument
    chdir(oldpwd)

    with pytest.raises(TypeError):
        chdir(1) # type: ignore

    with pytest.raises(DirectoryNotFoundError):
        chdir(tmp_path / "does_not_exist")

    with pytest.raises(NotADirectoryError):
        fp = tmp_path / "somefile"
        fp.write_text("some text")
        chdir(fp)

@pytest.fixture(scope="class")
def container():
    return XDictContainer({
        '1': {
            '1': 1,
            '2': 2
        },
        '2': {
            '1': 1,
            '2': 2
        }
    })

@pytest.fixture(scope="class")
def it_container(container: XDictContainer):
    return iter(container)

class TestXDictContainer:
    WHOLE_DICT: StrDict[StrDict[int]] = {'1': {'1': 1, '2': 2}, '2': {'1': 1, '2': 2}}
    SUB_DICT: StrDict[int] = {'1': 1, '2': 2}

    def test_get(self, container: XDictContainer):
        missing = object()

        value = container.get('1')
        match value:
            case {'1': 1, '2': 2}:
                pass

            case _:
                pytest.fail(f"invalid structure: {value!r}")

        # Get two different values and assert them
        value = container.get('1/1', missing)
        assert value is not missing
        value = container.get('2/1', missing)
        assert value is not missing

        # Get a value and assert it's the correct value
        value = container['2/2']
        assert value == 2

    @pytest.mark.parametrize(
        "expected,i",
        [(('1', SUB_DICT, WHOLE_DICT), 0),
         (('1', 1, SUB_DICT), 1),
         (('2', 2, SUB_DICT), 2),
         (('2', SUB_DICT, WHOLE_DICT), 3),
         (('1', 1, SUB_DICT), 4),
         (('2', 2, SUB_DICT), 5),]
    )
    def test_iter(self, expected: tuple[str, StrDict[int], StrDict[StrDict[int]]],
                  i: int, it_container: XDictContainer.XDictIterator):
        ek, ev, ep = expected
        k, v, p = next(it_container)

        assert k == ek, f"expected '{ek}', got '{k}' (test {i})"
        assert v == ev, f"expected {ev!r}, got {v!r} (test {i})"
        assert p == ep, f"expected {ep!r}, got {p!r} (test {i})"

    def test_iter_with_list(self):
        xdct = XDictContainer({'section': {
            'items': [1, 2, 3]
        }})

        # Skip first iteration
        it = iter(xdct)
        next(it)

        k, v, _, = next(it)
        assert v == [1, 2, 3]

    def test_errors(self, container: XDictContainer):
        with pytest.raises(StopIteration):
            it = iter(container)
            while True:
                next(it)

        with pytest.raises(KeyError):
            container['3']

        with pytest.raises(KeyError):
            container['1/3']

    def test_misc(self, container: XDictContainer):
        assert repr(container) == "XDictContainer({'1': {'1': 1, '2': 2}, '2': {'1': 1, '2': 2}})"

        match container.data:
            case {'1': {'1': 1, '2': 2}, '2': {'1': 1, '2': 2}}:
                pass

            case _:
                pytest.fail(f"invalid structure: {container.data!r}")
