"""Command-line interface."""
import logging
from typing import Optional

import coloredlogs
import typer

from mqsense import __version__

logger = logging.getLogger("mqsense")
app = typer.Typer()


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"mqsense: {__version__}")
        raise typer.Exit()


@app.callback()
def cli(
    version: Optional[bool] = typer.Option(  # noqa: B008, F841
        None, "--version", callback=version_callback, is_eager=True
    ),
    log_level: str = "INFO",
) -> None:
    """Command-line interface."""
    coloredlogs.install(level=log_level.upper())


def main() -> None:
    app()


if __name__ == "__main__":
    main()


# Sample typer subcommand 'hello'
# @app.command()
# def hello() -> None:
#     """sample command hello"""
#     logging.info("Hello")
