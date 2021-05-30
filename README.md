<div align="center">

<h1>Rubric</h1>
<strong>>> <i>Automate the boilerplate while initializing your Python project</i> <<</strong>

</div>


## Preface

Rubric is an opinionated project initializer for Python. It assumes that you'll use:

* Black as the primary code formatter.
* Isort to sort the imports.
* Flake8 to ensure style guide conformance.
* Mypy to check the type hints.
* Pip-tools to manage the dependencies.

Following is a list of config files that Rubric is going to add to your directory. The files will contain minimal but sensible default configurations for the respective tools. You're free to change them as you like.

```
root
├── .flake8                  # Config file for .flake8
├── .gitignore               # Python specific .gitignore file
├── makefile                 # Makefile to lint your code
├── mypy.ini                 # Config file for mypy type checker
├── pyproject.toml           # Toml file to hold a few common config vars
├── README.md                # A readme boilerplate
├── requirements-dev.txt     # File to specify the dev requirements
├── requirements.in          # File to specify the top level app requirements
└── requirements.txt         # File to specify the pinned app requirements
```


## Installation

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

    usage: rubric [-h] [--dirname DIRNAME] [--overwrite] run

    Rubric -- Initialize your Python project ⚙️

    positional arguments:
    run                run rubric & initialize the project scaffold

    optional arguments:
    -h, --help         show this help message and exit
    --dirname DIRNAME  target directory name
    --overwrite        overwrite existing linter config files

    ```

* Initialize your project with the following command:

    ```
    rubric run
    ```

    This will run the tool in a non-destructive way—that means it won't overwrite any of the configuration files that you might have in the directory.

    If you want to overwrite any of the existing config files that you might have in the directory, then run:

    ```
    rubric run --overwrite
    ```

    You can also point Rubric to a directory.

    ```
    rubric run --directory="some/custom/directory"
    ```

<div align="center">
<i> ✨ 🍰 ✨ </i>
</div>
