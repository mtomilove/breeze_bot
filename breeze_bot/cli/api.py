import click
from dotenv import load_dotenv

from breeze_bot.app.server import uvicorn_server


@click.group()
def start() -> None:
    """Запуск api приложения"""


@start.command()
def api() -> None:
    load_dotenv()
    uvicorn_server.run()
