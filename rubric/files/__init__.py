# This init is required by importlib
from __future__ import annotations

import argparse
import asyncio
import importlib.resources
import shutil
import sys
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import pkg_resources

FILE_GALLERY = [
    ".editorconfig",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    "README.md",
    "Makefile",
    "pyproject.toml",
    "requirements-dev.in",
    "requirements-dev.txt",
    "requirements.in",
    "requirements.txt",
]

TERMINAL_COLUMN_SIZE: int = shutil.get_terminal_size().columns


def _copy_over(
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


async def copy_over(
    src_filename: str,
    dst_dirname: str = ".",
    overwrite: bool = False,
    append: bool = False,
) -> None:
    """
    Creates a file named 'src_file' in the 'dst_dirname' directory and
    looks into the 'rubric' directory to see if there is a file with the same
    name as 'src_file' exists. If the file exists then it copies the contents
    of the file over to 'dst_dirname/src_filename'.
    """

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, _copy_over, src_filename, dst_dirname, overwrite, append
    )


def _display(filename: str) -> None:
    """Prints the contents of the config files."""

    with importlib.resources.open_text("rubric.files", filename) as file:

        decor = "="
        prefix = decor * ((TERMINAL_COLUMN_SIZE - len(filename)) // 2 - 10)
        print(
            f"\n{prefix} {filename} {prefix}\n\n",
            file.read(),
            end="",
            sep="",
        )


async def display(filename: str) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _display, filename)


async def orchestrator(
    dst_dirname: str,
    filenames: list = FILE_GALLERY,  # Infra filenames.
    overwrite: bool = False,
    append: bool = False,
    show: bool = False,
) -> None:

    """
    Diplays / Creates / Overwrites / Appends to the files listed
    in the 'FileGallery' asynchronously.
    """

    if show:
        tasks = [display(filename) for filename in filenames]
    else:
        tasks = [
            copy_over(src_filename, dst_dirname, overwrite, append)
            for src_filename in filenames
        ]

    await asyncio.gather(*tasks)


class CLI:
    def __init__(
        self,
        func: Callable[..., Awaitable[None]] = orchestrator,
        filenames: list = FILE_GALLERY,
    ) -> None:
        self.func = func
        self.filenames = filenames

    @property
    def header(self) -> None:
        """CLI header class."""
        ethos = ">> Linter Config Initializer for Python <<"

        print(
            "\n",
            "\033[1m",
            ethos.center(TERMINAL_COLUMN_SIZE - 11),
            "\033[0m",
            end="\n\n",
        )

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            add_help=False,
        )

        # Add arguments.
        parser.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show this help message and exit.",
        )

        # Add arguments.
        parser.add_argument(
            "run",
            help="Run rubric & initialize the project scaffold.",
            nargs="?",
        )

        parser.add_argument(
            "-l",
            "--list",
            help="List the config files that are about to be generated.",
            action="store_true",
        )
        parser.add_argument(
            "-d",
            "--dirname",
            help="Target directory name.",
            metavar="",
        )

        parser.add_argument(
            "-f",
            "--filename",
            help=(
                "Target file names. Allowed values are: "
                f"all, {', '.join(x for x in self.filenames)}."
            ),
            nargs="+",
            default=["all"],
            metavar="",
        )

        parser.add_argument(
            "-o",
            "--overwrite",
            help=(
                "Overwrite existing config files. Allowed values are the "
                "same as the values accepted by the '-f/--file' flag."
            ),
            nargs="+",
            metavar="",
        )

        parser.add_argument(
            "-a",
            "--append",
            help=(
                "Append to existing config files. Allowed values are the "
                "same as the values accepted by the '-f/--file' flag."
            ),
            nargs="+",
            metavar="",
        )

        parser.add_argument(
            "-s",
            "--show",
            help=(
                "Display the config file contents. Allowed values are the "
                "same as the values accepted by the '-f/--file' flag."
            ),
            nargs="+",
            metavar="",
        )

        parser.add_argument(
            "-v",
            "--version",
            help="Display the version number.",
            action="store_true",
        )

        return parser

    def handle_argerr(
        self,
        parser: argparse.ArgumentParser,
        args: argparse.Namespace,
    ) -> None:

        default = ["all"]
        if args.filename != default and not args.run:
            parser.error("'-f/--filename' cannot be used without 'run'")

        if args.dirname and not args.run:
            parser.error("'-d/--dirname' cannot be used without 'run'")

        if args.overwrite and not args.run:
            parser.error("'-o/--overwrite' cannot be used without 'run'")

        if args.append and not args.run:
            parser.error("'-a/--append' cannot be used without 'run'")

        if args.filename != default and args.overwrite:
            parser.error("'-f/--filename' and '-o/overwrite' cannot be used together")

        if args.filename != default and args.append:
            parser.error("'-f/--filename' and '-a/append' cannot be used together")

        if args.list and args.run:
            parser.error("'-l/--list' and 'run' cannot be used together")

        if args.show and args.run:
            parser.error("'-s/--show' and 'run' cannot be used together")

        if args.version and args.run:
            parser.error("'-v/--version' and 'run' cannot be used together")

        if args.list and args.version:
            parser.error("'-l/--list' and '-v/--version' cannot be used together")

        if args.list and args.show:
            parser.error("'-l/--list' and '-s/--show' cannot be used together")

        if args.version and args.show:
            parser.error("'-v/--version' and '-s/--show' cannot be used together")

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

        show = args.show
        if show and show != ["all"]:
            filtered_filenames = show

        filename = args.filename
        if filename != ["all"]:
            filtered_filenames = filename

        overwrite = args.overwrite
        if overwrite and overwrite != ["all"]:
            filtered_filenames = overwrite

        append = args.append
        if append and append != ["all"]:
            filtered_filenames = append

        dst_dirname = "."
        if args.dirname:
            dst_dirname = args.dirname

        # Actions based on the CLI arguments.
        if args.list:
            print("Config files that are about to be generated:\n")
            for filename in filtered_filenames:
                print(f"=> {filename}")

        if args.show:
            self.run_target(parser, dst_dirname, filtered_filenames, show=True)

        if args.run == "run":
            if args.overwrite:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                    overwrite=True,
                )
            elif args.append:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                    append=True,
                )
            else:
                self.run_target(
                    parser,
                    dst_dirname,
                    filtered_filenames,
                )


def cli_entrypoint(argv: list[str] | None = None) -> None:
    """CLI entrypoint callable."""
    cli = CLI()
    cli.entrypoint(argv)


if __name__ == "__main__":
    cli_entrypoint()
