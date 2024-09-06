import typer


app = typer.Typer(pretty_exceptions_show_locals=False)


# FIXME
@app.command()
def _main():
    pass


def main():
    from .telegram_api import backup  # noqa

    app()
