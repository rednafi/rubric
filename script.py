from enum import Enum


class InfraFile(str, Enum):
    def __new__(cls, value, description=""):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    FLAKE8 = ".flake8", "File containing the flake8 configs."
    GITIGNORE = ".gitignore", "Python specific .gitignore file."
    README = "README.md", "Minimalistic readme template."
    MAKEFILE = "makefile", "Makefile containing a few orchestration commands."
    PYPROJECT_TOML = "pyproject.toml", "Toml file containing black & mypy configs."
    REQ_DEV_IN = "requirements-dev.in", "In file containing the top-level dev deps."
    REQ_APP_IN = "requirements.in", "In file containing the top-level app deps."
    REQ_DEV_TXT = "requirements-dev.txt", "Txt file containing the pinned dev deps."
    REQ_APP_TXT = "requirements.txt", "Txt file containing the pinned app deps."
