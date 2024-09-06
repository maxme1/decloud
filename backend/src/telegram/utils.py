from ..settings import settings


MISSING_FILE = '(File not included. Change data exporting settings to download.)'


def file_url(x: str) -> str | None:
    if x is None or x == MISSING_FILE:
        return None
    return f'{settings.base_url}/files/telegram/' + x.removeprefix('storage/')
