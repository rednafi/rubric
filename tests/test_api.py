import pytest

import rubric


@pytest.fixture()
def create_file(tmp_path, filename):
    """Fixture to create a file in the tmp_path/tmp directory."""

    directory = tmp_path / "tmp"
    directory.mkdir()
    file = directory / filename  # request.param is the filename to be created
    return file


def test_filenames():
    expected_filenames = (
        ".editorconfig",
        ".gitignore",
        ".pre-commit-config.yaml",
        "README.md",
        "Makefile",
        "pyproject.toml",
        "requirements-dev.txt",
        "requirements.txt",
    )

    current_filenames = rubric.FILENAMES

    assert current_filenames == expected_filenames


@pytest.mark.parametrize("filename", ["pyproject.toml"])
def test_copy_over(create_file):
    file = create_file
    directory = file.parent

    # Creates a file in the temporary directory and copies the contents
    # of rubric/pyproject.toml file to it.
    rubric.copy_over("pyproject.toml", dst_dirname=str(directory))
    assert len(list(directory.iterdir())) == 1

    # Test the content of the pyproject.toml file.
    assert "follow_imports" in file.read_text()
    assert "mypy" in file.read_text()

    # Raises filenotfound error when the target name of the file
    # doesn't exist in the rubric/ directory.
    with pytest.raises(FileNotFoundError):
        rubric.copy_over("pypro.toml", dst_dirname=str(directory))


@pytest.mark.parametrize("filename", ["pyproject.toml"])
def test_copy_over_overwrite(create_file):
    file = create_file
    directory = file.parent

    file.write_text("Lorem ipsum!")
    assert "Lorem ipsum!" in file.read_text()

    # Creates a file in the temporary directory and copies the contents of
    # pyproject.toml file in it.
    rubric.copy_over("pyproject.toml", dst_dirname=str(directory), overwrite=True)
    assert len(list(directory.iterdir())) == 1

    assert "Lorem ipsum!" not in file.read_text()
    assert "tool.ruff" in file.read_text()


@pytest.mark.parametrize("filename", ["pyproject.toml"])
def test_copy_over_append(create_file):
    file = create_file
    directory = file.parent

    file.write_text("Lorem ipsum!")
    assert "Lorem ipsum!" in file.read_text()

    # Creates a file in the temporary directory and copies the contents
    # of rubric/mypy.ini file to it
    rubric.copy_over("pyproject.toml", dst_dirname=str(directory), append=True)
    assert len(list(directory.iterdir())) == 1

    assert "Lorem ipsum!" in file.read_text()
    assert "tool.ruff" in file.read_text()


@pytest.mark.parametrize("filename", ["pyproject.toml", "README.md"])
@pytest.mark.parametrize(
    ("overwrite", "append"),
    [(False, False), (True, False), (False, True), (True, True)],
)
def test_orcherstrator(create_file, overwrite, append):
    file = create_file
    directory = file.parent

    # This should copy all the files from rubric/ to the temporary directory.
    rubric.orchestrator(dst_dirname=str(directory), overwrite=overwrite, append=append)

    # Check whether there are all the files in the directory.
    assert len(list(directory.iterdir())) == len(rubric.FILENAMES)

    # Assert file contents.
    assert (
        any(
            term
            for term in ("tool.ruff", "center", "pip-tools")
            if term in file.read_text()
        )
        is True
    )


@pytest.mark.parametrize("filename", ["pyproject.toml", "README.md"])
@pytest.mark.parametrize(("overwrite", "append"), [(True, False)])
def test_orcherstrator_overwrite(
    create_file,
    overwrite,
    append,
):
    file = create_file
    directory = file.parent
    file.write_text("Lorem ipsum!")

    assert "Lorem ipsum!" in file.read_text()

    # This should copy all the files from rubric/ to the temporary directory.
    rubric.orchestrator(
        dst_dirname=str(directory),
        overwrite=overwrite,
        append=append,
    )

    # Check whether there are all the files in the directory.
    assert len(list(directory.iterdir())) == len(rubric.FILENAMES)

    # Assert file contents.
    assert (
        any(
            term
            for term in ("tool.ruff", "center", "pip-tools")
            if term in file.read_text()
        )
        is True
    )

    assert "Lorem ipsum!" not in file.read_text()


@pytest.mark.parametrize("filename", ["pyproject.toml", "README.md"])
@pytest.mark.parametrize(("overwrite", "append"), [(False, True)])
def test_orcherstrator_append(create_file, overwrite, append):
    file = create_file
    directory = file.parent

    file.write_text("Lorem ipsum!")

    assert "Lorem ipsum!" in file.read_text()

    # This should copy all the files from rubric/ to the temporary directory.
    rubric.orchestrator(
        dst_dirname=str(directory),
        overwrite=overwrite,
        append=append,
    )

    # Check whether there are all the files in the directory.
    assert len(list(directory.iterdir())) == len(rubric.FILENAMES)

    # Assert file contents.
    assert (
        any(
            term
            for term in ("tool.ruff", "center", "pip-tools")
            if term in file.read_text()
        )
        is True
    )

    assert "Lorem ipsum!" in file.read_text()


def test_display(capsys):
    for filename in ("pyproject.toml", "README.md"):
        rubric.display_content(filename)

    capture = capsys.readouterr()
    out = capture.out

    for tool in ("ruff", "mypy", "black"):
        assert tool in out

    assert "lorem ipsum" in out
    assert "pip-tools" in out
