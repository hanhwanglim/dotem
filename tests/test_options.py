from typer.testing import CliRunner
from dotem import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output == "0.1.0\n"
