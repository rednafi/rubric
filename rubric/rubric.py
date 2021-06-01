from __future__ import annotations

import argparse
import asyncio
import importlib.resources
import sys
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

import aiofiles

FILE_NAMES = (
    ".flake8",
    ".gitignore",
    "README.md",
    "makefile",
    "mypy.ini",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements.in",
    "requirements.txt",
)


async def create_file(
    filename: str,
    dirname: str = ".",
    overwrite: bool = False,
) -> None:
    """
    Creates a file and copies the contents of the file
    having the same name in the `rsrc` directory.

    Parameters
    ----------
    file_name : str
        File name that needs to be created.
    dir_name : str, optional
        Target directory name where the file should be created, by default ".".

    """

    if dirname:
        dirname = dirname.rstrip("/")

    # Do nothing, if the file already exists.
    if not overwrite:
        if Path(f"{dirname}/{filename}").exists():
            print(f"file {filename} already exists, skipping...")
            return

    with importlib.resources.open_text("rubric", filename) as src_file:
        async with aiofiles.open(f"{dirname}/{filename}", "w+") as dst_file:
            print(f"creating {filename}...")
            await dst_file.write(src_file.read())


async def consumer(dirname: str, overwrite: bool) -> None:
    """
    Create files defined in the `FILE_NAMES` asynchronously.

    Parameters
    ----------
    dir_name : str
        Target directory name where the file should be created.
    """
    tasks = [create_file(filename, dirname, overwrite) for filename in FILE_NAMES]

    await asyncio.gather(*tasks)


class CLI:
    def __init__(
        self,
        func: Callable[[str, bool], Coroutine[Any, Any, None]] = consumer,
    ) -> None:
        self.func = func

    @property
    def header(self):
        """CLI header class."""

        # Raw string to escape a few string formatting errors.
        print(
            r"""
           ___       __       _
          / _ \__ __/ /  ____(_)___
         / , _/ // / _ \/ __/ / __/
        /_/|_|\_,_/_.__/_/ /_/\__/
        """
        )

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="\nRubric -- Initialize your Python project ⚙️\n"
        )

        # Add arguments.
        parser.add_argument(
            "run",
            help="run rubric & initialize the project scaffold",
        )
        parser.add_argument("--dirname", help="target directory name")
        parser.add_argument(
            "--overwrite",
            help="overwrite existing linter config files",
            action="store_true",
        )

        return parser

    def entrypoint(self, argv: list[str] | None = None) -> None:
        self.header
        parser = self.build_parser()

        # Run help when the entrypoint command is called w/o any argument.
        if not argv:
            parser.parse_args(args=None if sys.argv[1:] else ["--help"])
            args = parser.parse_args()
        else:
            args = parser.parse_args(argv)

        _dir_name = args.dirname
        _overwrite = args.overwrite
        dir_name = _dir_name if _dir_name else "."
        overwrite = _overwrite if _overwrite else False

        if args.run == "run":
            asyncio.run(self.func(dir_name, overwrite))


def cli_entrypoint(argv: list[str] | None = None) -> None:
    """CLI entrypoint callable."""
    cli = CLI()
    cli.entrypoint(argv)


if __name__ == "__main__":
    cli_entrypoint()
