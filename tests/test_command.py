import os
import shutil
from contextlib import contextmanager, suppress
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from dotem import app
from tests.data import TEST_DATA

runner = CliRunner()


@contextmanager
def temporary_copy_file(src: Path, dest: Path) -> None:
    try:
        with suppress(FileNotFoundError):
            os.remove(dest)

        shutil.copyfile(src, dest)
        yield
    finally:
        with suppress(FileNotFoundError):
            os.remove(dest)


class TestLoad:
    def test_load_default(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["load"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "export hate-dandruff=false",
                "export bloomers-handbook='awake lifting decrease grid'",
                "export volumes-unruly=15",
                "export companion-esteemed=0.95",
                "export glowworm-flashback=a",
                "export fidelity-starch=true\n",
            ]

    def test_load_default_with_path(self) -> None:
        result = runner.invoke(app, ["load", "--path", f"{TEST_DATA / 'data.toml'}"])
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "export hate-dandruff=false",
            "export bloomers-handbook='awake lifting decrease grid'",
            "export volumes-unruly=15",
            "export companion-esteemed=0.95",
            "export glowworm-flashback=a",
            "export fidelity-starch=true\n",
        ]


class TestUnload:
    def test_unload_default(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["unload"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "unset hate-dandruff",
                "unset bloomers-handbook",
                "unset volumes-unruly",
                "unset companion-esteemed",
                "unset glowworm-flashback",
                "unset fidelity-starch\n",
            ]

    def test_unload_default_with_path(self) -> None:
        result = runner.invoke(app, ["unload", "--path", f"{TEST_DATA / 'data.toml'}"])
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "unset hate-dandruff",
            "unset bloomers-handbook",
            "unset volumes-unruly",
            "unset companion-esteemed",
            "unset glowworm-flashback",
            "unset fidelity-starch\n",
        ]

    def test_unload_all(self) -> None:
        result = runner.invoke(
            app, ["unload", "--all", "--path", f"{TEST_DATA / 'data.toml'}"]
        )
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "unset hate-dandruff",
            "unset bloomers-handbook",
            "unset volumes-unruly",
            "unset companion-esteemed",
            "unset glowworm-flashback",
            "unset fidelity-starch",
            "unset deport-nuzzle",
            "unset FOLLOW_CYCLING",
            "unset parchment-blazing",
            "unset judo-abridge",
            "unset SECRET_PASSWORD",
            "unset KEY",
            "unset hello",
            "unset foo\n",
        ]


def test_edit() -> None:
    with patch("dotem.click.edit") as click_patch:
        result = runner.invoke(app, ["edit"])
        click_patch.assert_called()
        assert result.exit_code == 0
