import typer
import importlib.metadata
from typing_extensions import Annotated, Optional

app = typer.Typer()


def version_callback(value: bool) -> None:
    if not value:
        return
    print(importlib.metadata.version("dotem"))
    raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show version information."
        ),
    ] = None,
):
    pass


if __name__ == "__main__":
    app()
