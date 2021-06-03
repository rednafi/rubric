from __future__ import annotations

import argparse
import asyncio
import importlib.resources
import sys
from collections.abc import Callable, Coroutine, Iterable
from pathlib import Path
from typing import Any

import aiofiles

FILENAMES = (
    ".flake8",
    ".gitignore",
    "README.md",
    "makefile",
    "mypy.ini",
    "pyproject.toml",
    "requirements-dev.in",
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
            print(f"File {filename} already exists, skipping...")
            return

    dst_filepath = f"{dirname}/{filename}"

    with importlib.resources.open_text("rubric", filename) as src_file:
        async with aiofiles.open(dst_filepath, "w+") as dst_file:
            print(f"Creating {filename}...")
            await dst_file.write(src_file.read())


async def consumer(
    dirname: str,
    filenames: Iterable[str] = FILENAMES,
    overwrite: bool = False,
) -> None:
    """
    Create files defined in the `FILE_NAMES` asynchronously.

    Parameters
    ----------
    dir_name : str
        Target directory name where the file should be created.
    """
    tasks = [create_file(filename, dirname, overwrite) for filename in filenames]

    await asyncio.gather(*tasks)


class CLI:
    def __init__(
        self,
        func: Callable[..., Coroutine[Any, Any, None]] = consumer,
        filenames: Iterable[str] = FILENAMES,
    ) -> None:
        self.func = func
        self.filenames = filenames

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
            description="\nRubric -- Initialize your Python project ⚙️\n",
        )

        # Add arguments.
        parser.add_argument(
            "run",
            help="run rubric & initialize the project scaffold",
            nargs="?",
        )
        parser.add_argument(
            "--list",
            help="list the config files that are about to be generated",
            action="store_true",
        )
        parser.add_argument(
            "--dirname",
            help="target directory name",
            default=".",
        )
        parser.add_argument(
            "--overwrite",
            help=(
                "overwrite existing config files, "
                "allowed values are: all, " + ", ".join(str(x) for x in self.filenames)
            ),
            nargs="+",
        )

        return parser

    def error_handlers(
        self,
        parser: argparse.ArgumentParser,
        args: argparse.Namespace,
    ) -> None:

        if args.list and args.run:
            parser.error("argument `list` and `run` cannot be used together")

        if args.list and args.overwrite:
            parser.error("argument `list` and `overwrite` cannot be used together")

        if args.overwrite and not args.run:
            parser.error("argument `overwrite` cannot be used without argument `run`")

        if args.dirname and not args.run:
            parser.error("argument `dirname` cannot be used without argument `run`")

        if args.overwrite and args.overwrite != ["all"]:
            filtered_filenames = args.overwrite
            for filtered_filename in filtered_filenames:
                if filtered_filename not in self.filenames:
                    parser.error(
                        f"filename {filtered_filename} is not valid\n"
                        "Run rubric --list to see the allowed filenames"
                    )

    def entrypoint(self, argv: list[str] | None = None) -> None:
        self.header
        parser = self.build_parser()

        # Run help when the entrypoint command is called w/o any argument.
        if not argv:
            parser.parse_args(args=None if sys.argv[1:] else ["--help"])
            args = parser.parse_args()
        else:
            args = parser.parse_args(argv)

        # Handling pesky argument inconsistency errors.
        self.error_handlers(parser, args)

        filtered_filenames = self.filenames

        overwrite = args.overwrite
        if overwrite and overwrite != ["all"]:
            filtered_filenames = overwrite

        if args.run == "run":
            if args.overwrite:
                asyncio.run(
                    self.func(args.dirname, filtered_filenames, overwrite=True),
                )
            else:
                asyncio.run(
                    self.func(args.dirname, filtered_filenames, overwrite=False),
                )

        if args.list:
            print("config files that are about to be generated:\n")
            for filename in filtered_filenames:
                print(f"=> {filename}")


def cli_entrypoint(argv: list[str] | None = None) -> None:
    """CLI entrypoint callable."""
    cli = CLI()
    cli.entrypoint(argv)


if __name__ == "__main__":
    cli_entrypoint()
