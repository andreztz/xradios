import socket
import subprocess
import sys
import time

import click
from jsonrpclib import Server

from xradios.__about__ import __version__
from xradios.ui import UI


def is_server_running(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (ConnectionRefusedError, OSError):
        return False


def start_server(host, port):
    proc = subprocess.Popen(
        ["xradiosd", "--host", host, "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc


@click.command()
@click.version_option(version=__version__, prog_name="xradios")
@click.option(
    "--host", default="127.0.0.1", help="Server address (default: 127.0.0.1)"
)
@click.option(
    "--port", default=10000, type=int, help="Server port (default: 10000)"
)
def main(host, port):
    proc = None

    if host in {"127.0.0.1", "0.0.0.0"}:
        if not is_server_running(host, port):
            proc = start_server(host, port)

    client = Server(f"http://{host}:{port}")

    for _ in range(10):
        try:
            if client.ping() == "pong":
                break
        except ConnectionRefusedError:
            time.sleep(1)
    else:
        click.secho(
            "The server did not respond after multiple attempts.",
            fg="red",
        )
        sys.exit(1)

    app = UI(client)
    app.run()

    if proc is not None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
