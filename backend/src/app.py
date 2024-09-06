import deli
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from .static import serve
from .interface import ChatInfo, ChatInterface
from .schema import AgentMessage, SystemMessage
from .settings import settings
from .slack.interface import Slack  # noqa
from .telegram.interface import Telegram  # noqa


class TypeSchemaApp(FastAPI):
    def openapi(self):
        api = super().openapi()
        for schema in api['components']['schemas'].values():
            if 'type' in schema.get('properties', ()):
                schema['required'] = list(set(schema.get('required', ())) | {'type'})

        return api


app = TypeSchemaApp()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=['*'],
)


class Chat(BaseModel):
    id: str
    name: str
    source: str


chats_list = [
                 Chat(id=x, name=y, source='telegram')
                 for x, y in deli.load(settings.telegram_root / 'chats.json').items()
             ] + [
                 Chat(id=x['id'], name=x['name'], source='slack')
                 for x in sorted(deli.load(settings.slack_root / 'conversations.json'), key=lambda x: -x['updated'])
                 if not x['is_archived']
             ]


@app.get('/chats')
async def chats() -> list[Chat]:
    return chats_list


@app.get('/messages/{source}/{chat_id}')
async def messages(source: str, chat_id: str) -> list[AgentMessage | SystemMessage]:
    chat = ChatInterface.find(source)
    result = []
    for msg in chat.load(chat_id)[-500:]:
        # if msg.get('media_type') not in ['video_file', 'audio_file', 'voice_message', 'animation', 'video_message']:
        #     continue
        try:
            msg = chat.validate(msg)
        except Exception as e:
            raise RuntimeError(msg) from e

        ready = chat.convert(msg)
        # if not any(x.type in ('file', 'image', 'video', 'audio') for x in ready.blocks):
        #     continue

        result.append(ready)

    return result


@app.get('/info/{source}/{chat_id}')
async def info(source: str, chat_id: str) -> ChatInfo:
    chat = ChatInterface.find(source)
    return chat.info(chat_id)


@app.get('/files/{source}/{identifier}', response_class=Response, include_in_schema=False)
async def _static(request: Request, source: str, identifier: str):
    chat = ChatInterface.find(source)
    absolute, kind = chat.resolve(identifier)
    return serve(request, absolute, kind)
