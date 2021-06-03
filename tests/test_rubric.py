import pytest

from rubric import rubric


@pytest.mark.asyncio
async def test_create_file(tmp_path):
    d = tmp_path / "dest"
    d.mkdir()
    p = d / "mypy.ini"

    # Creates a file in the temporary directory and copies the contents
    # of rubric/mypy.ini file to it
    await rubric.create_file("mypy.ini", dirname=str(d))
    assert len(list(d.iterdir())) == 1

    # Test the content of the mypy.ini file.
    assert "follow_imports" and "mypy" in p.read_text()

    # Raises filenotfound error when the target name of the file
    # doesn't exist in the rubric/ directory.
    with pytest.raises(FileNotFoundError):
        await rubric.create_file("myp.ini", dirname=str(d))


@pytest.mark.asyncio
async def test_consumer(tmp_path):
    d = tmp_path / "dest"
    d.mkdir()

    p = d / "pyproject.toml"
    q = d / "README.md"
    r = d / "requirements-dev.in"

    # This should copy all the files from rubric/ to the temporary directory.
    await rubric.consumer(dirname=str(d), overwrite=True)

    # Check whether there are all the files in the directory.
    assert len(list(d.iterdir())) == len(rubric.FILENAMES)

    # Assert file contents.
    assert "tool.isort" in p.read_text()
    assert "center" in q.read_text()
    assert "pip-tools" in r.read_text()


def test_cli_entrypoint(tmp_path, capsys):
    d = tmp_path / "dest"
    d.mkdir()

    rubric.cli_entrypoint(["run", f"--dirname={str(d)}"])
    capture = capsys.readouterr()
    out = capture.out

    assert r"____(_)___" in out
    assert r"creating" or "exists" in out
