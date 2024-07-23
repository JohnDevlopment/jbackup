from __future__ import annotations
from . import APPNAME

import typer

app = typer.Typer(name=APPNAME)

@app.command()
def backup() -> int:
    return 0

if __name__ == '__main__':
    raise NotImplementedError
