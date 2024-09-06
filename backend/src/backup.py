import typer


app = typer.Typer(pretty_exceptions_show_locals=False)


def main():
    from .telegram_api import backup  # noqa
    from .slack import backup  # noqa

    app()
