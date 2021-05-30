from __future__ import annotations

import argparse
import asyncio
import importlib.resources
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

import aiofiles

FILE_NAMES = (
    "requirements.in",
    "requirements.txt",
    "requirements-dev.txt",
    "makefile",
    ".flake8",
    "mypy.ini",
    "pyproject.toml",
    ".gitignore",
)


async def create_file(
    filename: str, dirname: str = ".", overwrite: bool = False
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
        dirname = dirname.strip("/")

    # Do nothing, if the file already exists.
    if not overwrite:
        if Path(f"{dirname}/{filename}").exists():
            print(f"file {filename} already exists, skipping...")
            return

    with importlib.resources.open_text("rsrc", filename) as src_file:
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
    await asyncio.gather(
        *[
            create_file(
                filename,
                dirname,
                overwrite,
            )
            for filename in FILE_NAMES
        ],
    )


class CLI:
    def __init__(
        self,
        func: Callable[[str, bool], Coroutine[Any, Any, None]] = consumer,
    ) -> None:
        self.func = func

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="\nEpigraph -- Initialize your Python project ⚙️\n"
        )

        # Add arguments.
        parser.add_argument("--dirname", help="target directory name")
        parser.add_argument(
            "--overwrite",
            help="overwrite existing linter config files",
            action="store_true",
        )

        return parser

    def entrypoint(self) -> None:
        parser = self.build_parser()
        args = parser.parse_args()

        _dir_name = args.dirname
        _overwrite = args.overwrite
        dir_name = _dir_name if _dir_name else "."
        overwrite = _overwrite if _overwrite else False
        asyncio.run(self.func(dir_name, overwrite))


cli = CLI()
cli.entrypoint()
