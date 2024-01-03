import os
import platform
import re
import shlex
import sys
from collections import namedtuple
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

EnvironmentVariable = namedtuple("EnvironmentVariable", ["key", "value"])

SHELL_VARIABLE_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def parse_booleans(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def validate_env_var(env_var: EnvironmentVariable) -> bool:
    return bool(re.match(SHELL_VARIABLE_REGEX, env_var.key))


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


def load_variables(
    config: Dict[str, Any], profile: List[str]
) -> List[EnvironmentVariable]:
    variables: List[EnvironmentVariable] = []

    for key, value in config.pop("global", {}).items():
        variables.append(EnvironmentVariable(key, shlex.quote(parse_booleans(value))))

    def walk(_config: Dict[str, Any], _profile: Optional[List[str]]) -> None:
        for _key, _value in _config.items():
            if not isinstance(_value, dict):
                variables.append(
                    EnvironmentVariable(_key, shlex.quote(parse_booleans(_value)))
                )
            elif _profile is None:
                walk(_value, _profile)
            elif _profile[0] == _key:
                walk(_value, profile[1:])

    walk(config, profile)

    for variable in variables:
        if not validate_env_var(variable):
            raise ValueError(f"Invalid environment variable: {variable.key}")

    return variables


@app.command()
def load(
    profile: Annotated[str, typer.Argument(help="Profile to load.")] = "default",
    path: Annotated[
        Optional[str], typer.Option(show_default=False, help="Dotenv toml path.")
    ] = None,
    set_all: Annotated[
        Optional[bool],
        typer.Option("--all", help="Load all environment variables in toml file."),
    ] = False,
) -> None:
    """Loads the environment variables set in the profile."""
    config = load_config(path)

    if profile is None:
        profile = "default"
    profile = None if set_all else profile.split(".")

    try:
        environment_variables = load_variables(config, profile)
    except ValueError as exc:
        print(exc)
        raise typer.Exit(1)

    environment_variables = [
        f"export {key}={value}" for key, value in environment_variables
    ]
    print(";".join(environment_variables))


@app.command()
def unload(
    profile: Annotated[str, typer.Argument(help="Profile to unload.")] = "default",
    path: Annotated[
        Optional[str], typer.Option(show_default=False, help="Dotenv toml path.")
    ] = None,
    unset_all: Annotated[
        Optional[bool],
        typer.Option("--all", help="Unload all environment variables in toml file."),
    ] = False,
) -> None:
    """Unset the environment variables set in the profile"""
    config = load_config(path)

    if profile is None:
        profile = "default"
    profile = None if unset_all else profile.split(".")

    try:
        environment_variables = load_variables(config, profile)
    except ValueError as exc:
        print(exc)
        raise typer.Exit(1)

    environment_variables = [f"unset {key}" for key, _ in environment_variables]
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
