from functools import cache

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from .interface import Chat, ChatInfo, ChatInterface
from .schema import AnyMessage
from .slack.interface import Slack  # noqa
from .static import serve
from .telegram.interface import Telegram  # noqa
from .telegram_api.interface import TelegramAPI


class TypeSchemaApp(FastAPI):
    def openapi(self):
        api = super().openapi()
        for schema in api['components']['schemas'].values():
            for prop in 'type', 'event':
                if prop in schema.get('properties', ()):
                    schema['required'] = list(set(schema.get('required', ())) | {prop})

        return api


app = TypeSchemaApp()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=['*'],
)


@cache
def get_agents(interface):
    return ChatInterface.find(interface).gather_agents()


@app.get('/chats')
async def chats() -> list[Chat]:
    return TelegramAPI().gather_chats()  # + Telegram().gather_chats()  # + Slack().gather_chats()


@app.get('/messages/{source}/{chat_id}')
async def messages(source: str, chat_id: str) -> list[AnyMessage]:
    chat = ChatInterface.find(source)
    result = []
    for msg in chat.load(chat_id):
        # if 'reply_to' not in msg:
        #     continue
        # if msg.get('media_type') != 'video_file':
        #     # if 'cashtag' not in str(msg):
        #     # if not msg.get('location_information'):
        #     continue

        # print(msg.get('edited'))
        # if msg.get('media_type') not in ['video_file', 'audio_file', 'voice_message', 'animation', 'video_message']:
        #     continue
        # if not msg.get('attachments'):
        #     continue

        try:
            msg = chat.validate(msg)
        except Exception as e:
            raise RuntimeError(msg) from e

        ready = chat.convert(msg)
        # if ']:(' not in str(ready):
        #     continue

        # if not any(x.type in ('file', 'image', 'video', 'audio') for x in ready.blocks):
        #     continue
        # if 'ATTACHMENT: !!!!' not in str(ready):
        #     continue

        result.append(ready)
        # if len(result) > 10:
        #     break

    return result


@app.get('/info/{source}/{chat_id}')
async def info(source: str, chat_id: str) -> ChatInfo:
    return ChatInfo(agents=get_agents(source))


@app.get('/files/{source}/{identifier}', response_class=Response, include_in_schema=False)
async def _static(request: Request, source: str, identifier: str):
    chat = ChatInterface.find(source)
    absolute, kind = chat.resolve(identifier)
    return serve(request, absolute, kind)
