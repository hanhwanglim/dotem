import os
import shutil
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import Iterator
from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from dotem import app
from tests import TEST_DIR
from tests.data import TEST_DATA

runner = CliRunner()


@contextmanager
def temporary_copy_file(src: Path, dest: Path) -> Iterator[None]:
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
                "export hate_dandruff=false",
                "export bloomers_handbook='awake lifting decrease grid'",
                "export volumes_unruly=15",
                "export companion_esteemed=0.95",
                "export glowworm_flashback=a",
                "export fidelity_starch=true\n",
            ]

    def test_load_default_with_path(self) -> None:
        result = runner.invoke(app, ["load", "--path", f"{TEST_DATA / 'data.toml'}"])
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "export hate_dandruff=false",
            "export bloomers_handbook='awake lifting decrease grid'",
            "export volumes_unruly=15",
            "export companion_esteemed=0.95",
            "export glowworm_flashback=a",
            "export fidelity_starch=true\n",
        ]

    def test_load_group_a(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["load", "group-a"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "export hate_dandruff=false",
                "export bloomers_handbook='awake lifting decrease grid'",
                "export volumes_unruly=15",
                "export companion_esteemed=0.95",
                "export deport_nuzzle='lorem ipsum'",
                "export FOLLOW_CYCLING=10\n",
            ]

    def test_load_group_a_with_path(self) -> None:
        result = runner.invoke(
            app, ["load", "group-a", "--path", f"{TEST_DATA / 'data.toml'}"]
        )
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "export hate_dandruff=false",
            "export bloomers_handbook='awake lifting decrease grid'",
            "export volumes_unruly=15",
            "export companion_esteemed=0.95",
            "export deport_nuzzle='lorem ipsum'",
            "export FOLLOW_CYCLING=10\n",
        ]

    def test_load_subgroup_1(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["load", "group-b.subgroup-1"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "export hate_dandruff=false",
                "export bloomers_handbook='awake lifting decrease grid'",
                "export volumes_unruly=15",
                "export companion_esteemed=0.95",
                "export parchment_blazing='HELLO WORLD'",
                "export judo_abridge=true",
                "export SECRET_PASSWORD=password",
                "export KEY=VALUE\n",
            ]

    def test_load_subgroup_2_with_path(self) -> None:
        result = runner.invoke(
            app, ["load", "group-b.subgroup-2", "--path", f"{TEST_DATA / 'data.toml'}"]
        )
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "export hate_dandruff=false",
            "export bloomers_handbook='awake lifting decrease grid'",
            "export volumes_unruly=15",
            "export companion_esteemed=0.95",
            "export parchment_blazing='HELLO WORLD'",
            "export judo_abridge=true",
            "export hello=world",
            "export foo=bar\n",
        ]

    def test_load_invalid(self) -> None:
        result = runner.invoke(app, ["load", "--path", f"{TEST_DATA / 'invalid.toml'}"])
        assert result.exit_code == 1
        assert result.output.split(";") == [
            "Invalid environment variable: hate-dandruff\n"
        ]


class TestUnload:
    def test_unload_default(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["unload"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "unset hate_dandruff",
                "unset bloomers_handbook",
                "unset volumes_unruly",
                "unset companion_esteemed",
                "unset glowworm_flashback",
                "unset fidelity_starch\n",
            ]

    def test_unload_default_with_path(self) -> None:
        result = runner.invoke(app, ["unload", "--path", f"{TEST_DATA / 'data.toml'}"])
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "unset hate_dandruff",
            "unset bloomers_handbook",
            "unset volumes_unruly",
            "unset companion_esteemed",
            "unset glowworm_flashback",
            "unset fidelity_starch\n",
        ]

    def test_unload_group_a(self) -> None:
        src = TEST_DATA / "data.toml"
        dest = Path(os.getcwd()) / ".env.toml"

        with temporary_copy_file(src, dest):
            result = runner.invoke(app, ["unload", "group-a"])
            assert result.exit_code == 0
            assert result.output.split(";") == [
                "unset hate_dandruff",
                "unset bloomers_handbook",
                "unset volumes_unruly",
                "unset companion_esteemed",
                "unset deport_nuzzle",
                "unset FOLLOW_CYCLING\n",
            ]

    def test_unload_group_a_with_path(self) -> None:
        result = runner.invoke(
            app, ["unload", "group-a", "--path", f"{TEST_DATA / 'data.toml'}"]
        )
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "unset hate_dandruff",
            "unset bloomers_handbook",
            "unset volumes_unruly",
            "unset companion_esteemed",
            "unset deport_nuzzle",
            "unset FOLLOW_CYCLING\n",
        ]

    def test_unload_all(self) -> None:
        result = runner.invoke(
            app, ["unload", "--all", "--path", f"{TEST_DATA / 'data.toml'}"]
        )
        assert result.exit_code == 0
        assert result.output.split(";") == [
            "unset hate_dandruff",
            "unset bloomers_handbook",
            "unset volumes_unruly",
            "unset companion_esteemed",
            "unset glowworm_flashback",
            "unset fidelity_starch",
            "unset deport_nuzzle",
            "unset FOLLOW_CYCLING",
            "unset parchment_blazing",
            "unset judo_abridge",
            "unset SECRET_PASSWORD",
            "unset KEY",
            "unset hello",
            "unset foo\n",
        ]

    def test_unload_invalid(self) -> None:
        result = runner.invoke(
            app, ["unload", "--path", f"{TEST_DATA / 'invalid.toml'}"]
        )
        assert result.exit_code == 1
        assert result.output.split(";") == [
            "Invalid environment variable: hate-dandruff\n"
        ]


@patch("dotem.click.edit")
def test_edit(edit_patch: MagicMock) -> None:
    src = TEST_DATA / "data.toml"
    dest = Path(os.getcwd()) / ".env.toml"

    with temporary_copy_file(src, dest):
        result = runner.invoke(app, ["edit"])

    edit_patch.assert_called()
    assert result.exit_code == 0


def test_hook() -> None:
    result = runner.invoke(app, ["hook"])
    assert result.exit_code == 0
    with open(TEST_DIR.parent / "hook.sh") as f:
        assert result.output == f.read() + "\n"
