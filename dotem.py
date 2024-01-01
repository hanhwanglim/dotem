import os
import platform
import shlex
import sys
from pathlib import Path

import click
import typer
import importlib.metadata

from typing import List, Any, Dict, Optional
from typing_extensions import Annotated

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


def find_file() -> Optional[Path]:
    """Tries to find the `.env.toml` file

    The search order is: cwd -> parent directory -> $XDG_CONFIG_HOME -> $HOME
    """
    cwd = Path(os.getcwd())
    parent = cwd.parent
    xdg_config_home = Path(
        os.getenv("XDG_CONFIG_HOME", Path.home() / ".config" / "dotem")
    )
    home = Path.home()

    directories: List[Path] = [cwd, parent, xdg_config_home, home]

    for directory in directories:
        if (directory / ".env.toml").exists():
            return directory / ".env.toml"
    raise FileNotFoundError("Unable to find `.env.toml` file")


def load_config(path: Optional[str]) -> Dict[str, Any]:
    try:
        path = find_file() if path is None else Path(path)
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        print("Unable to find `.env.toml` file. Please specify `--path`")
        raise typer.Exit(1)
    except tomllib.TOMLDecodeError as exc:
        print(f"Unable to parse file: {exc}")
        raise typer.Exit(1)


@app.command()
def load(
    profile: Annotated[str, typer.Argument(help="Profile to load.")] = "default",
    path: Annotated[
        Optional[str], typer.Option(show_default=False, help="Dotenv toml path.")
    ] = None,
) -> None:
    """Loads the environment variables set in the profile."""
    config = load_config(path)
    environment_variables: List[str] = []

    for key, value in config.get("global", {}).items():
        export = f"export {key}={shlex.quote(parse_booleans(value))}"
        environment_variables.append(export)

    for key, value in config[profile].items():
        export = f"export {key}={shlex.quote(parse_booleans(value))}"
        environment_variables.append(export)

    print(";".join(environment_variables))


@app.command()
def unload(
    profile: Annotated[str, typer.Argument(help="Profile to unload.")] = "default",
    path: Annotated[
        Optional[str], typer.Option(show_default=False, help="Dotenv toml path.")
    ] = None,
    unset_all: Annotated[
        Optional[bool],
        typer.Option("--all", help="Unload all environment variables in toml file"),
    ] = False,
) -> None:
    """Unset the environment variables set in the profile"""
    config = load_config(path)

    environment_variables: List[str] = []

    def walk(obj: Dict[str, Any]):
        for key, value in obj.items():
            if isinstance(value, dict):
                walk(value)
            else:
                environment_variables.append(f"unset {key}")

    if not unset_all:
        for key in config.get("global", {}):
            environment_variables.append(f"unset {key}")

        for key in config[profile]:
            environment_variables.append(f"unset {key}")
    else:
        walk(config)

    print(";".join(environment_variables))


@app.command()
def edit(
    path: Annotated[
        Optional[str], typer.Option(show_default=False, help="Dotenv toml path.")
    ] = None,
    editor: Annotated[
        Optional[str], typer.Option(show_default=False, help="Editor.")
    ] = None,
) -> None:
    """Edits the `.env.toml` file in `$EDITOR`"""
    try:
        path = find_file() if path is None else Path(path)
    except FileNotFoundError:
        print("Unable to find `.env.toml` file. Please specify `--path`")
        raise typer.Exit(1)

    click.edit(editor=editor, filename=path)


@app.command()
def hook() -> None:
    """Script to help set up the shell hook"""
    with open(Path(__file__).parent / "hook.sh") as script:
        print(script.read())


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
) -> None:
    pass


def main() -> None:
    app(prog_name="dotem")


if __name__ == "__main__":
    main()
