import typer


app = typer.Typer(pretty_exceptions_show_locals=False)


def main():
    from .slack import backup  # noqa
    from .telegram_sdk import backup  # noqa

    app()
