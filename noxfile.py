"""Nox sessions."""
import sys
from pathlib import Path
from textwrap import dedent


try:
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None

import nox
from nox.sessions import Session

package = "mqsense"
python_versions = ["3.9"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = "lint", "safety", "tests"
locations = "src", "tests", "noxfile.py"


TEST_DEPS = [
    "pytest",
    "coverage[toml]",
    "pytest-cov",
    "pytest-mock",
]


@session(python="3.9")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python="3.9")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "flake8-json",
        "flake8-codeclimate",
    )
    session.run("flake8", *args)


@session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", "--full-report", f"--file={requirements}")


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(*TEST_DEPS)
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_versions)
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".")
    session.install("pytest", "typeguard", "pygments")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


owner, repository = "alexandervantrijffel", "mqsense"
labels = "mqsense"
bump_paths = "README.rst"


@nox.session(name="prepare-release")
def prepare_release(session: Session) -> None:
    """Prepare a GitHub release."""
    args = [
        f"--owner={owner}",
        f"--repository={repository}",
        *[f"--bump={path}" for path in bump_paths],
        *[f"--label={label}" for label in labels],
        *session.posargs,
    ]
    session.install("click", "github3.py")
    session.run("python", "tools/prepare-github-release.py", *args, external=True)


@nox.session(name="publish-release")
def publish_release(session: Session) -> None:
    """Publish a GitHub release."""
    args = [f"--owner={owner}", f"--repository={repository}", *session.posargs]
    session.install("click", "github3.py")
    session.run("python", "tools/publish-github-release.py", *args, external=True)
