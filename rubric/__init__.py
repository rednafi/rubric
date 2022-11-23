from __future__ import annotations

import importlib.resources
import shutil
from pathlib import Path
from typing import Iterable

import click
import pkg_resources
import sys

FILENAMES = (
    ".editorconfig",
    ".gitignore",
    ".pre-commit-config.yaml",
    "README.md",
    "Makefile",
    "pyproject.toml",
    "requirements-dev.in",
    "requirements-dev.txt",
    "requirements.in",
    "requirements.txt",
)

TERMINAL_COLUMN_SIZE: int = shutil.get_terminal_size().columns

def copy_over(
    src_filename: str,
    dst_dirname: str = ".",
    overwrite: bool = False,
    append: bool = False,
) -> None:

    """
    This function takes 'src_filename' and 'dst_dirname' where they mean
    source file name and destination directory name respectively.

    First, it searches in the 'rubric' directory to check if there is
    a file that exists with the same name as the 'src_filename'. If the file
    exists, it creates another file named 'src_filename' in the 'dst_dirname'
    and copies over the content of the file in the 'rubric' directory.
    """

    if dst_dirname:
        dst_dirname = dst_dirname.rstrip("/")

    dst_filepath = f"{dst_dirname}/{src_filename}"

    # Do nothing, if the file already exists.
    if not overwrite and not append:
        if Path(dst_filepath).exists():
            print(f"File {src_filename} already exists, skipping...")
            return None

    open_mode = "w+"
    if append:
        open_mode = "a+"

    # We use importlib here so that we don't have to deal with making
    # sure Python can find the `rubric` directory when this is installed
    # as a CLI.
    with importlib.resources.open_text("rubric.files", src_filename) as src_file:
        with open(dst_filepath, open_mode) as dst_file:

            if open_mode == "w+":
                if overwrite:
                    print(f"Overwriting {src_filename}...")
                else:
                    print(f"Creating {src_filename}...")
            else:
                print(f"Appending to {src_filename}...")

            dst_file.write(src_file.read())


def list_filenames(
    ctx: click.Context,
    param: click.Parameter | None,  # noqa
    value: bool,
    filenames: Iterable[str] = FILENAMES,
) -> None:
    """Callback to list the names of the config files."""

    if not value or ctx.resilient_parsing:
        return

    click.echo("Config files that are about to be generated:\n")
    for filename in filenames:
        print(f"=> {filename}")
    ctx.exit()


def display_version(
    ctx: click.Context,
    param: click.Parameter | None,  # noqa
    value: bool,
) -> None:
    """Callback to display the version number of the CLI."""

    if not value or ctx.resilient_parsing:
        return

    __version__ = pkg_resources.get_distribution("rubric").version
    print(f"version: {__version__}")
    ctx.exit()


def display_help(
    ctx: click.Context,
    param: click.Parameter | None,  # noqa
    value: bool,
) -> None:
    if value is False:
        return

    ethos = ">> Config Initializer for Python Projects <<"
    decor = " "
    pad = decor * ((TERMINAL_COLUMN_SIZE - len(ethos)) // 2 - 8)
    click.echo(f"{pad}{ethos}{pad}\n", color=True)
    click.echo(ctx.get_help())
    ctx.exit()


def display_content(filename: str) -> None:
    """Prints the contents of the config files."""

    with importlib.resources.open_text("rubric.files", filename) as file:
        decor = "="
        pad = decor * ((TERMINAL_COLUMN_SIZE - len(filename)) // 2 - 10)
        print(
            f"\n{pad} {filename} {pad}\n\n",
            file.read(),
            end="",
            sep="",
        )


def orchestrator(
    dst_dirname: str,
    filenames: Iterable[str] = FILENAMES,  # Infra filenames.
    overwrite: bool = False,
    append: bool = False,
    show: bool = False,
) -> None:

    """
    Display / Create / Overwrite / Append to the files listed
    in the 'FILENAMES' iterable.
    """

    if show:
        for filename in filenames:
            display_content(filename)
    else:
        for src_filename in filenames:
            copy_over(src_filename, dst_dirname, overwrite, append)


@click.command()
@click.option(
    "--help",
    "-h",
    is_flag=True,
    expose_value=False,
    is_eager=False,
    callback=display_help,
    help="Display help message.",
)
@click.option(
    "--version",
    "-v",
    is_flag=True,
    default=False,
    expose_value=False,
    callback=display_version,
    help="Display the version number.",
)
@click.option(
    "--show",
    "-s",
    is_flag=True,
    default=False,
    help="Show the contents of the config files.",
)
@click.option(
    "--append",
    "-a",
    is_flag=True,
    default=False,
    help="Append to existing config files.",
)
@click.option(
    "--overwrite",
    "-o",
    is_flag=True,
    default=False,
    help="Overwrite existing config files.",
)
@click.option(
    "--create",
    "-c",
    default=False,
    is_flag=True,
    help="Create the config files in the current directory.",
)
@click.option(
    "--filename",
    "-f",
    multiple=True,
    type=click.Choice(FILENAMES),
    help="Target file names.",
)
@click.option(
    "--dirname",
    "-d",
    type=click.Path(exists=True),
    default=".",
    help="Target directory name.",
)
@click.option(
    "--list",
    "-l",
    default=False,
    is_flag=True,
    callback=list_filenames,
    help="List the config files that are about to be generated.",
)
@click.pass_context
def cli(
    ctx: click.Context,
    list: bool,
    dirname: str,
    filename: str,
    create: bool,
    overwrite: bool,
    append: bool,
    show: bool,
) -> None:

    # Display help text when there's no flag.
    if not any((list, create, overwrite, append, show)):
        display_help(ctx, None, True)

    if create and any((show, overwrite, append)):
        if show:
            raise click.UsageError(
                "Cannot use '--create' / '-c' and '--show' / '-s' together."
            )
        if overwrite:
            raise click.UsageError(
                "Cannot use '--create' / '-c' and '--overwrite' / '-o' together."
            )
        if append:
            raise click.UsageError(
                "Cannot use '--create' / '-c' and '--append' / '-a' together."
            )

    if list and show:
        raise click.UsageError(
            "Cannot use '--list' / '-l' and '--show' / '-s' together."
        )

    if overwrite and show:
        raise click.UsageError(
            "Cannot use '--overwrite' / '-o'  and '--show' / '-s' together."
        )

    if append and overwrite:
        raise click.UsageError(
            "Cannot use '--append' / '-a' and '--overrite' / '-o' together."
        )

    if append and show:
        raise click.UsageError(
            "Cannot use '--append' / '-a' and '--show' / '-s' together."
        )

    # Call handlers.
    files = filename if filename else FILENAMES

    if overwrite:
        return orchestrator(dst_dirname=dirname, filenames=files, overwrite=overwrite)

    if append:
        return orchestrator(dst_dirname=dirname, filenames=files, append=append)

    if show:
        return orchestrator(dst_dirname=dirname, filenames=files, show=show)

    if create and not any((show, overwrite, append)):
        return orchestrator(dst_dirname=dirname, filenames=files)


if __name__ == "__main__":
    cli()
