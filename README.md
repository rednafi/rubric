
<div align="center">

<h1>Rubric</h1>
<strong>>> <i>Linter Config Initializer for Python</i> <<</strong>

&nbsp;

</div>

![img](https://user-images.githubusercontent.com/30027932/122619075-6a87b700-d0b1-11eb-9d6b-355446910cc1.png)


## Preface

Rubric initializes the configuration files of a few Python linters and formatters. Also, it adds a README.md boilerplace and a simple Makefile with the commands to apply the tools. This helps you maintain an isomorphic workflow across multiple projects. It assumes that, in all of your Python projects, you'll use—

* [Black](https://github.com/psf/black) as the primary code formatter.
* [EditorConfig](https://editorconfig.org/) to enforce consistent coding styles for multiple developers.
* [Isort](https://github.com/PyCQA/isort) to sort the imports.
* [Flake8](https://github.com/PyCQA/flake8) to ensure style guide conformance.
* [Mypy](https://github.com/python/mypy) to check the type hints.
* [Pip-tools](https://github.com/jazzband/pip-tools) to manage the dependencies.
* [Pre-commit](https://pre-commit.com/) for managing and maintaining the pre-commit hooks.


Following is a list of config files that Rubric is going to add to your target directory:

```
root
├── .editorconfig           # Config file for Editorconfig
├── .flake8                 # Config file for .flake8
├── .gitignore              # Python specific .gitignore file
├── .pre-commit-config.yaml # Config to manage pre-commit hooks.
├── Makefile                # Makefile containing the commands to lint your code
├── pyproject.toml          # Toml file to with the configs for mypy, black & isort
├── README.md               # A readme boilerplate
├── requirements-dev.in     # File to specify the top level dev requirements
├── requirements-dev.txt    # File to specify the dev requirements
├── requirements.in         # File to specify the top level app requirements
└── requirements.txt        # File to specify the pinned app requirements
```

The files will contain minimal but sensible default configurations for the respective tools. You're free to change them as you like.

## Installation

* Rubric requires Python 3.8 and up.

* Make a virtual environment in your project's root directory.

* Activate the environment and run:

    ```
    pip install rubric
    ```

## Usage

* To inspect all the CLI options, run:

    ```
    rubric --help
    ```

    You should see the following output:

    ```
                >> Linter Config Initializer for Python <<

    usage: rubric [-h] [-l] [-d] [-f  [...]] [-o  [...]] [-a  [...]] [-s  [...]]
                [-v]
                [run]

    positional arguments:
    run                   Run rubric & initialize the project scaffold.

    optional arguments:
    -h, --help            Show this help message and exit.
    -l, --list            List the config files that are about to be
                            generated.
    -d , --dirname        Target directory name.
    -f  [ ...], --filename  [ ...]
                            Target file names. Allowed values are: all,
                            .editorconfig, .flake8, .gitignore, .pre-commit-
                            config.yaml, README.md, Makefile, pyproject.toml,
                            requirements-dev.in, requirements-dev.txt,
                            requirements.in, requirements.txt.
    -o  [ ...], --overwrite  [ ...]
                            Overwrite existing config files. Allowed values are
                            the same as the values accepted by the '-f/--file'
                            flag.
    -a  [ ...], --append  [ ...]
                            Append to existing config files. Allowed values are
                            the same as the values accepted by the '-f/--file'
                            flag.
    -s  [ ...], --show  [ ...]
                            Display the config file contents. Allowed values are
                            the same as the values accepted by the '-f/--file'
                            flag.
    -v, --version         Display the version number.
    ```

* Display a list of config files that are going to be created:

    ```
    rubric --list
    ```

    ```
    $ rubric --list

                        >> Linter Config Initializer for Python <<

    Config files that are about to be generated:

    => .editorconfig
    => .flake8
    => .gitignore
    => .pre-commit-config.yaml
    => README.md
    => Makefile
    => pyproject.toml
    => requirements-dev.in
    => requirements-dev.txt
    => requirements.in
    => requirements.txt    ```

* Take a peek into the content of any config file(s):
    ```
    rubric --show .flake8 requirements-dev.in
    ```

    This will print:

    ```
                >> Linter Config Initializer for Python <<

    ================================= .flake8 =================================

    [flake8]
    extend-exclude =
        .git,
        __pycache__,
        docs/source/conf.py,
        old,
        build,
        dist,
        .venv,
        venv

    extend-ignore = E203, E266, E501, W605

    # Black's default line length.
    max-line-length = 88

    max-complexity = 18

    # Specify the list of error codes you wish Flake8 to report.
    select = B,C,E,F,W,T4,B9

    # Parallelism
    jobs = 4

    =========================== requirements-dev.in ===========================

    # For linting.
    black
    flake8
    isort
    mypy
    pre-commit

    # For dep management.
    pip-tools

    # For testing.
    pytest
    pytest-asyncio

    # For building & uploading to PyPI.
    twine
    build

    ```


* Initialize a project with the following command:

    ```
    rubric run
    ```

    This will run the tool in a non-destructive way—that means it won't overwrite any of the configuration files that you might have in the directory.

* If you only want to create a selected list of config files, then run:

    ```
    rubric run -f requirements*
    ```

* If you want to overwrite any of the existing config files that you might have in the directory, then run:

    ```
    rubric run --overwrite filename1 filename2
    ```

* If you want to append the configs to an existing file, then run:

    ```
    rubric run --append filename1 filename2
    ```

* You can also point Rubric to a directory.

    ```
    rubric run --directory "some/custom/directory"
    ```

* If you want to check and update the configs across multiple repositories in a single sweep, use the following command:

    ```
    s="dir1 dir2 dir3"; echo $s | xargs -n 1 -P $(echo $s | wc -w) rubric run -d
    ```

    This command will spawn 3 processes to create the config files in `dir1`, `dir2`, and `dir3` in parallel.

* You can run the entire linter suite with this command:

    ```
    make lint
    ```

<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
