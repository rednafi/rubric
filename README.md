<div align="center">

<h1>Rubric</h1>
<strong>>> <i>Automate the boilerplate while initializing your Python project</i> <<</strong>

</div>


## Preface

Rubric is an opinionated project initializer for Python. Following is a list of config files that Rubric is going to add to your directory:

```
root
├── .flake8
├── .gitignore
├── makefile
├── mypy.ini
├── pyproject.toml
├── README.md
├── requirements-dev.txt
├── requirements.in
└── requirements.txt
```


## Installation

* Make a virtual environment in your project's root director.

* Activate the environemnt and run:

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

    This will run the tool in a non-destructive way—that means it won't overwrite any of the configuration file that you might have in the directory.

    If you want to overwrite any of the existing config file that you might have in the directory, then run:

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
