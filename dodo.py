""" doit tasks for ipyradiant

    Generally, you'll just want to `doit`. See `doit list` for more options.
"""
import sys
from pathlib import Path

DOIT_CONFIG = {
    "backend": "sqlite3",
    "verbosity": 2,
    "par_type": "thread",
    # "default_tasks": ["binder"]
}


def task_setup():
    """ perform all setup activities
    """
    yield dict(
        name="js",
        file_dep=[P.YARN_LOCK, P.PACKAGE],
        actions=[[*P.JLPM, "--prefer-offline", "--ignore-optional"]],
        targets=[P.YARN_INTEGRITY],
    )
    yield dict(
        name="py",
        file_dep=[P.SETUP_PY, P.SETUP_CFG],
        actions=[[*P.PIP, "install", "-e", ".", "--no-deps"], [*P.PIP, "check"]],
    )


def task_lint():
    """ format all source files
    """
    yield dict(name="isort", file_dep=P.ALL_PY, actions=[["isort", "-rc", *P.ALL_PY]])
    yield dict(name="black", file_dep=P.ALL_PY, actions=[["black", *P.ALL_PY]])
    yield dict(name="flake8", file_dep=P.ALL_PY, actions=[["flake8", *P.ALL_PY]])
    yield dict(name="mypy", file_dep=P.ALL_PY_SRC, actions=[["mypy", *P.ALL_PY_SRC]])
    yield dict(name="pylint", file_dep=P.ALL_PY, actions=[["pylint", *P.ALL_PY]])
    yield dict(
        name="prettier",
        file_dep=[P.YARN_INTEGRITY, *P.ALL_PRETTIER],
        actions=[[*P.JLPM, "lint:prettier"]],
    )


# pylint: disable=invalid-name,too-few-public-methods
class P:
    """ important paths
    """

    DODO = Path(__file__)
    HERE = DODO.parent
    POSTBUILD = HERE / "postBuild"

    # tools
    PY = [Path(sys.executable)]
    PYM = [*PY, "-m"]
    PIP = [*PYM, "pip"]
    JLPM = ["jlpm"]

    NODE_MODULES = HERE / "node_modules"
    PACKAGE = HERE / "package.json"
    YARN_INTEGRITY = NODE_MODULES / ".yarn-integrity"
    YARN_LOCK = HERE / "yarn.lock"

    PY_SRC = HERE / "ipyradiant"
    SETUP_PY = HERE / "setup.py"
    SETUP_CFG = HERE / "setup.cfg"
    ALL_PY_SRC = [*PY_SRC.rglob("*.py")]
    ALL_PY = [DODO, POSTBUILD, *ALL_PY_SRC]
    ALL_YML = [*HERE.glob("*.yml")]
    ALL_JSON = [*HERE.glob("*.json")]
    ALL_PRETTIER = [*ALL_YML, *ALL_JSON]
