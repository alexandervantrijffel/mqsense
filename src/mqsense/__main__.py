"""Command-line interface."""
import datetime
import json
import logging
import random
from typing import Optional
import coloredlogs
import typer
from mqsense import __version__
from mqsense.mqttclient import ConnectionDetails, MQTTClient

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


def get_connection_details(host: str, user: str, password: str) -> ConnectionDetails:
    return ConnectionDetails(
        host,
        user,
        password,
        clientId=f"mqsense-{random.randrange(10000,999999,1)}",
    )


host_option = typer.Option(
    "localhost",
    "--host-name",
    "-h",
    envvar="MQSENSE_BROKER_HOST",
    help="Hostname to connect to. Example: test.mosquitto.org",
)

username_option = typer.Option(
    ...,
    "--user-name",
    "-u",
    envvar="MQSENSE_USERNAME",
    help="Username for connecting to the MQTT broker",
)

password_option = typer.Option(
    ...,
    "--password",
    "-p",
    envvar="MQSENSE_PASSWORD",
    help="Password for connecting to the MQTT broker",
)


@app.command()
def subscribe(
    host: str = host_option, user_name: str = username_option, password: str = password_option
) -> None:
    """subscribes to all topics on the broker"""
    MQTTClient().subscribe(get_connection_details(host, user_name, password), "#")


@app.command()
def publish(
    host: str = host_option, user_name: str = username_option, password: str = password_option
) -> None:
    MQTTClient().publish(
        get_connection_details(host, user_name, password),
        topic="mqsense/test",
        message=json.dumps(
            {"title": "this is just a test", "time": str(datetime.datetime.now().isoformat())},
        ),
    )


def main() -> None:
    app()


if __name__ == "__main__":
    app()
