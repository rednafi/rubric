from __future__ import annotations

import argparse
import asyncio
import importlib.resources
import sys
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

import pkg_resources

FILENAMES = (
    ".flake8",
    ".gitignore",
    "README.md",
    "makefile",
    "pyproject.toml",
    "requirements-dev.in",
    "requirements-dev.txt",
    "requirements.in",
    "requirements.txt",
)


def _copy_over(
    src_filename: str,
    dst_dirname: str = ".",
    overwrite: bool = False,
    append: bool = False,
) -> None:
    """
    This function takes `src_filename` and `dst_dirname` where they mean
    source file name and destination directory name respectively.

    First, it searches in the `rubric` directory to check if there is
    a file that exists with the same name as the `src_filename`. If the file
    exists, it creates another file named `src_filename` in the `dst_dirname`
    and copies over the content of the file in rubric directory.
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


async def copy_over(
    src_filename: str,
    dst_dirname: str = ".",
    overwrite: bool = False,
    append: bool = False,
) -> None:
    """
    Creates a file named `src_file` in the `dst_dirname` directory and
    looks into `rubric` directory to see if there is a file with the same
    name as `src_file` exists. If the file exists then it copies the contents
    of the file over to `dst_dirname/src_filename`.
    """

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, _copy_over, src_filename, dst_dirname, overwrite, append
    )


async def consumer(
    dst_dirname: str,
    filenames: tuple[str, ...] = FILENAMES,  # Allowed filenames.
    overwrite: bool = False,
    append: bool = False,
) -> None:
    """Creates / Overwrites / Appends to the files defined in the
    `FILE_NAMES` asynchronously.
    """

    tasks = [
        copy_over(src_filename, dst_dirname, overwrite, append)
        for src_filename in filenames
    ]

    await asyncio.gather(*tasks)


class CLI:
    def __init__(
        self,
        func: Callable[..., Coroutine[Any, Any, None]] = consumer,
        filenames: tuple[str, ...] = FILENAMES,
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
            "-l",
            "--list",
            help="list the config files that are about to be generated",
            action="store_true",
        )
        parser.add_argument(
            "-d",
            "--dirname",
            help="target directory name",
        )
        parser.add_argument(
            "-o",
            "--overwrite",
            help=(
                "overwrite existing config files, "
                "allowed values are: all, " + ", ".join(str(x) for x in self.filenames)
            ),
            nargs="+",
        )

        parser.add_argument(
            "-a",
            "--append",
            help=(
                "append to existing config files, "
                "allowed values are: all, " + ", ".join(str(x) for x in self.filenames)
            ),
            nargs="+",
        )

        parser.add_argument(
            "-v",
            "--version",
            help="display the version number",
            action="store_true",
        )

        return parser

    def handle_argerr(
        self,
        parser: argparse.ArgumentParser,
        args: argparse.Namespace,
    ) -> None:

        if args.overwrite and not args.run:
            parser.error("'-o/--overwrite' cannot be used without 'run'")

        if args.dirname and not args.run:
            parser.error("'-d/--dirname' cannot be used without 'run'")

        if args.append and not args.run:
            parser.error("'-a/--append' cannot be used without 'run'")

        if args.append and args.overwrite:
            parser.error("'-a/--append' and '-o/--overwrite' cannot be used together")

        if args.list and args.run:
            parser.error("'-l/--list' and 'run' cannot be used together")

        if args.list and args.version:
            parser.error("'-l/--list' and '-v/--version' cannot be used together")

        if args.version and args.run:
            parser.error("'-v/--version' and 'run' cannot be used together")

        if args.overwrite and args.overwrite != ["all"]:
            filtered_filenames = args.overwrite
            for filtered_filename in filtered_filenames:
                if filtered_filename not in self.filenames:
                    parser.error(
                        f"filename {filtered_filename} is not valid\n"
                        "Run rubric --list to see the allowed filenames"
                    )
        if args.version:
            __version__ = pkg_resources.get_distribution("rubric").version
            print(f"version: {__version__}")

    def run_target(
        self,
        parser: argparse.ArgumentParser,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run the `consumer` function."""

        try:
            asyncio.run(self.func(*args, **kwargs))
        except FileNotFoundError:
            parser.error("invalid file/directory name")

    def entrypoint(self, argv: list[str] | None = None) -> None:
        # Print the nice rubric header.
        self.header
        parser = self.build_parser()

        # Run help when the entrypoint command is called w/o any argument.
        if not argv:
            parser.parse_args(args=None if sys.argv[1:] else ["--help"])
            args = parser.parse_args()
        else:
            args = parser.parse_args(argv)

        # Handling pesky argument inconsistency errors.
        self.handle_argerr(parser, args)

        # Parsing the arguments.
        filtered_filenames = self.filenames
        overwrite = args.overwrite
        if overwrite and overwrite != ["all"]:
            filtered_filenames = overwrite

        append = args.append
        if append and append != ["all"]:
            filtered_filenames = append

        _dirname = args.dirname
        if _dirname:
            dst_dirname = _dirname
        else:
            dst_dirname = "."

        # Actions based on the CLI arguments.
        if args.list:
            print("config files that are about to be generated:\n")
            for filename in filtered_filenames:
                print(f"=> {filename}")

        if args.run == "run":
            if args.overwrite:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                    overwrite=True,
                    append=False,
                )
            elif args.append:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                    overwrite=False,
                    append=True,
                )
            else:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                    overwrite=False,
                    append=False,
                )


def cli_entrypoint(argv: list[str] | None = None) -> None:
    """CLI entrypoint callable."""
    cli = CLI()
    cli.entrypoint(argv)


if __name__ == "__main__":
    cli_entrypoint()
