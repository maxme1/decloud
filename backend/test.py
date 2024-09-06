from tqdm.auto import tqdm

from src.interface import ChatInterface


for interface in ChatInterface.all().values():
    bar = tqdm(interface.gather_chats(), desc=interface.name)
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
