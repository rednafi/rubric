<div align="center">

<h1>Rubric</h1>
<strong>>> <i>Automate the boilerplate while initializing your Python project</i> <<</strong>

&nbsp;

</div>

![img](https://images.unsplash.com/photo-1582184520153-cb662f665f11?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1850&q=80)

## Preface

Rubric is an opinionated project initializer for Python. It assumes that you'll use:

* [Black](https://github.com/psf/black) as the primary code formatter.
* [Isort](https://github.com/PyCQA/isort) to sort the imports.
* [Flake8](https://github.com/PyCQA/flake8) to ensure style guide conformance.
* [Mypy](https://github.com/python/mypy) to check the type hints.
* [Pip-tools](https://github.com/jazzband/pip-tools) to manage the dependencies.

Following is a list of config files that Rubric is going to add to your directory:

```
root
├── .flake8                  # Config file for .flake8
├── .gitignore               # Python specific .gitignore file
├── makefile                 # Makefile containing the commands to lint your code
├── mypy.ini                 # Config file for mypy type checker
├── pyproject.toml           # Toml file to hold a few common config vars
├── README.md                # A readme boilerplate
├── requirements-dev.in      # File to specify the top level dev requirements
├── requirements-dev.txt     # File to specify the dev requirements
├── requirements.in          # File to specify the top level app requirements
└── requirements.txt         # File to specify the pinned app requirements
```

The files will contain minimal but sensible default configurations for the respective tools. You're free to change them as you like.

## Installation

* Rubric requires Python 3.7 and up.

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
    $ rubric

           ___       __       _
          / _ \__ __/ /  ____(_)___
         / , _/ // / _ \/ __/ / __/
        /_/|_|\_,_/_.__/_/ /_/\__/

    usage: rubric [-h] [-l] [-d DIRNAME] [-o OVERWRITE [OVERWRITE ...]] [-v] [run]

    Rubric -- Initialize your Python project ⚙️

    positional arguments:
    run                   run rubric & initialize the project scaffold

    optional arguments:
    -h, --help            show this help message and exit
    -l, --list            list the config files that are about to be generated
    -d DIRNAME, --dirname DIRNAME
                            target directory name
    -o OVERWRITE [OVERWRITE ...], --overwrite OVERWRITE [OVERWRITE ...]
                            overwrite existing config files, allowed values are: all, .flake8,
                            .gitignore, README.md, makefile, mypy.ini, pyproject.toml,
                            requirements-dev.in, requirements-dev.txt, requirements.in,
                            requirements.txt
    -v, --version         display the version number

    ```

* Initialize a project with the following command:

    ```
    rubric run
    ```

    This will run the tool in a non-destructive way—that means it won't overwrite any of the configuration files that you might have in the directory.

    If you want to overwrite any of the existing config files that you might have in the directory, then run:

    ```
    rubric run --overwrite filename1 filename2
    ```

    You can also point Rubric to a directory.

    ```
    rubric run --directory "some/custom/directory"
    ```

<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
