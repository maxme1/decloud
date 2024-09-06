from tqdm.auto import tqdm

from backend.src.settings import settings
from backend.src.slack.interface import Slack
from backend.src.telegram.interface import Telegram
from backend.src.telegram_api.interface import TelegramAPI


interfaces = []
if settings.telegram_api_root:
    interfaces.append(TelegramAPI())
if settings.slack_root:
    interfaces.append(Slack())
if settings.telegram_root:
    interfaces.append(Telegram())

for interface in interfaces:
    bar = tqdm(interface.gather_chats(), desc=type(interface).__name__)
    for chat in bar:
        bar.set_postfix(chat=chat.name)
        for msg in interface.load(chat.id):
            try:
                msg = interface.validate(msg)
            except Exception as e:
                raise RuntimeError(msg, chat) from e

            try:
                ready = interface.convert(msg)
            except Exception as e:
                raise RuntimeError(msg, chat) from e
