import datetime
import uuid

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore
from llama_index.core.storage.chat_store import SimpleChatStore

from app.config import REDIS_HOST, REDIS_PORT


class Chat:
    def __init__(self, model, chatstore):
        self.model = model

        if not model.id:
            self.id = str(uuid.uuid4())
        else:
            self.id = model.id

        self.memory = ChatMemoryBuffer.from_defaults(token_limit=3900, chat_store=chatstore, chat_store_key="memory_" + self.id)

        self.created = datetime.datetime.now()

    def clear_history(self):
        self.memory.reset()

    def __eq__(self, other):
        return self.id == other.id
