from .message import *

MessageModel: dict[str, BaseMessage] = {
    'text': TextMessage,
    'image': ImageMessage,
    'voice': VoiceMessage,
    'video': VideoMessage,
    'location': LocationMessage,
    'link': LinkMessage
}

MsgTypes = ['text', 'image', 'voice', 'video', 'location', 'link']
