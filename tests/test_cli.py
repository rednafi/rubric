from unittest.mock import patch

from click.testing import CliRunner

import rubric


def test_cli_version():
    with patch(
        "rubric.display_version",
        autospec=True,
        return_value="version: 0.0.0\n",
    ):
        runner = CliRunner()
        result = runner.invoke(rubric.cli, ["--version"])
        assert result.exit_code == 0
        # assert result.output == "version: 0.0.0\n"
