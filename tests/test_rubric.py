from __future__ import annotations

from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from rubric import rubric


@pytest.mark.asyncio
async def test_copy_over_default(tmp_path: Path) -> None:
    print(type(tmp_path))
    d = tmp_path / "dest"
    d.mkdir()
    p = d / "pyproject.toml"

    # Creates a file in the temporary directory and copies the contents
    # of rubric/pyproject.toml file to it.
    await rubric.copy_over("pyproject.toml", dst_dirname=str(d))
    assert len(list(d.iterdir())) == 1

    # Test the content of the pyproject.toml file.
    assert "follow_imports" and "mypy" in p.read_text()

    # Raises filenotfound error when the target name of the file
    # doesn't exist in the rubric/ directory.
    with pytest.raises(FileNotFoundError):
        await rubric.copy_over("pypro.toml", dst_dirname=str(d))


@pytest.mark.asyncio
async def test_copy_over_overwrite(tmp_path: Path) -> None:
    d = tmp_path / "dest"
    d.mkdir()
    p = d / "pyproject.toml"

    p.write_text("Lorem ipsum!")
    assert "Lorem ipsum!" in p.read_text()

    # Creates a file in the temporary directory and copies the contents
    # of rubric/mypy.ini file to it
    await rubric.copy_over("pyproject.toml", dst_dirname=str(d), overwrite=True)
    assert len(list(d.iterdir())) == 1

    assert "Lorem ipsum!" not in p.read_text()
    assert "tool.black" in p.read_text()


@pytest.mark.asyncio
async def test_copy_over_append(tmp_path: Path) -> None:
    d = tmp_path / "dest"
    d.mkdir()
    p = d / "pyproject.toml"

    p.write_text("Lorem ipsum!")
    assert "Lorem ipsum!" in p.read_text()

    # Creates a file in the temporary directory and copies the contents
    # of rubric/mypy.ini file to it
    await rubric.copy_over("pyproject.toml", dst_dirname=str(d), append=True)
    assert len(list(d.iterdir())) == 1

    assert "Lorem ipsum!" in p.read_text()
    assert "tool.black" in p.read_text()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overwrite, append",
    [
        (False, False),
        (True, False),
        (False, True),
        (True, True)
    ],
)
async def test_consumer(tmp_path: Path, overwrite: bool, append: bool) -> None:
    d = tmp_path / "dest"
    d.mkdir()

    p = d / "pyproject.toml"
    q = d / "README.md"
    r = d / "requirements-dev.in"

    # This should copy all the files from rubric/ to the temporary directory.
    await rubric.consumer(dst_dirname=str(d), overwrite=overwrite, append=append)

    # Check whether there are all the files in the directory.
    assert len(list(d.iterdir())) == len(rubric.FILENAMES)

    # Assert file contents.
    assert "tool.isort" in p.read_text()
    assert "center" in q.read_text()
    assert "pip-tools" in r.read_text()


def test_cli_entrypoint(tmp_path: Path, capsys: CaptureFixture) -> None:
    d = tmp_path / "dest"
    d.mkdir()

    rubric.cli_entrypoint(["run", f"--dirname={str(d)}"])
    capture = capsys.readouterr()
    out = capture.out

    assert r"____(_)___" in out
    assert r"creating" or "exists" in out
