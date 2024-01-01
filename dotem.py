import platform
import shlex
import sys
from pathlib import Path

import typer
import importlib.metadata

from typing import List, Any
from typing_extensions import Annotated, Optional

if platform.system() not in ("Linux", "Darwin"):
    raise OSError("Unsupported operating system")

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

app = typer.Typer(
    help="dotem: A tool for loading dotenv environment variables into your shell."
)


def parse_booleans(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


@app.command()
def load(
    profile: Annotated[str, typer.Argument(help="Profile to load.")] = "default",
    path: Annotated[str, typer.Option(help="Dotenv toml path.")] = "./.env.toml",
) -> None:
    """Loads the environment variables set in the profile."""
    with open(Path(path), "rb") as f:
        config = tomllib.load(f)

    environment_variables: List[str] = []

    for key, value in config.get("global", {}).items():
        export = f"export {key}={shlex.quote(parse_booleans(value))}"
        environment_variables.append(export)

    for key, value in config[profile].items():
        export = f"export {key}={shlex.quote(parse_booleans(value))}"
        environment_variables.append(export)

    print(";".join(environment_variables))


def version_callback(value: bool) -> None:
    if not value:
        return
    print(f"{shlex.quote(importlib.metadata.version('dotem'))}")
    raise typer.Exit()


@app.callback()
def options(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", callback=version_callback, help="Show version information."
        ),
    ] = None,
):
    pass


def main() -> None:
    app(prog_name="dotem")


if __name__ == "__main__":
    main()
