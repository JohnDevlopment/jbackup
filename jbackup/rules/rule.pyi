from pathlib import Path
from typing import Any, Literal, overload
from ..types import StrPath
from .config.config_protocol import ConfigFile

class Rule:
    @overload
    def __init__(self, filename: StrPath, mode: Literal['r']) -> None:
        ...

    @overload
    def __init__(self, filename: StrPath, mode: Literal['w'],
                 data: dict[str, Any]) -> None:
        ...

    @staticmethod
    def get_path() -> Path:
        ...

    @classmethod
    @overload
    def find(cls, name: str) -> Path:
        ...

    @classmethod
    @overload
    def find(cls, name: str, read: Literal[True]) -> Rule:
        ...

    @property
    def config(self) -> ConfigFile:
        ...

    def get(self, key: str, default: Any=..., safe: bool=...) -> Any:
        ...

    def __getitem__(self, key: str) -> Any:
        ...
