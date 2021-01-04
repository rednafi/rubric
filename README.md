
<div align="center">

<h1>Rubric</h1>
<strong>>> <i>Effortless Config Initializer for Isomorphic Python Projects</i> <<</strong>

&nbsp;

</div>

![img](https://user-images.githubusercontent.com/30027932/122619075-6a87b700-d0b1-11eb-9d6b-355446910cc1.png)


## Preface

Rubric is a minimalistic project initializer and configuration conformity checker that helps you initialize, maintain, and enforce the same configuration structure across multiple Python projects. It can come in handy when you're maintaining several Python projects, and you want to make sure all the linting and management workflows are isomorphic and deterministic across different repositories.

It doesn't enforce any source code structure. Rather it just assumes that—you'd want to use the following tools to lint and manage your code—and adds a bunch of sensible configuration to your project's root folder:

* [Black](https://github.com/psf/black) as the primary code formatter.
* [Isort](https://github.com/PyCQA/isort) to sort the imports.
* [Flake8](https://github.com/PyCQA/flake8) to ensure style guide conformance.
* [Mypy](https://github.com/python/mypy) to check the type hints.
* [Pip-tools](https://github.com/jazzband/pip-tools) to manage the dependencies.

Following is a list of config files that Rubric is going to add to your target directory:

```
root
├── .flake8                # Config file for .flake8
├── .gitignore             # Python specific .gitignore file
├── makefile               # Makefile containing the commands to lint your code
├── pyproject.toml         # Toml file to with the configs for mypy, black & isort
├── README.md              # A readme boilerplate
├── requirements-dev.in    # File to specify the top level dev requirements
├── requirements-dev.txt   # File to specify the dev requirements
├── requirements.in        # File to specify the top level app requirements
└── requirements.txt       # File to specify the pinned app requirements
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
           ___       __       _
          / _ \__ __/ /  ____(_)___
         / , _/ // / _ \/ __/ / __/
        /_/|_|\_,_/_.__/_/ /_/\__/

    usage: rubric [-h] [-l] [-d DIRNAME] [-o OVERWRITE [OVERWRITE ...]]
                [-a APPEND [APPEND ...]] [-v]
                [run]

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
                            .gitignore, README.md, makefile, pyproject.toml, requirements-
                            dev.in, requirements-dev.txt, requirements.in, requirements.txt
    -a APPEND [APPEND ...], --append APPEND [APPEND ...]
                            append to existing config files, allowed values are: all, .flake8,
                            .gitignore, README.md, makefile, pyproject.toml, requirements-
                            dev.in, requirements-dev.txt, requirements.in, requirements.txt
    -v, --version         display the version number
    ```
* Take a peek into the config files that are going to be created:

    ```
    rubric --list
    ```

    ```
    config files that are about to be generated:

    => .flake8
    => .gitignore
    => README.md
    => makefile
    => pyproject.toml
    => requirements-dev.in
    => requirements-dev.txt
    => requirements.in
    => requirements.txt
    ```

* Initialize a project with the following command:

    ```
    rubric run
    ```

    This will run the tool in a non-destructive way—that means it won't overwrite any of the configuration files that you might have in the directory.

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
