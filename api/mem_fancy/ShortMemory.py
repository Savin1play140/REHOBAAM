import random
from api.utils.Functions import GTTSCM_IH
from api.remote_client.OllamaClient import OllamaClient

class ShortMemory:
	def __init__(self, model: str, ollama: OllamaClient):
		self._chat = {}
		self._model = model
		self._last_msgid = 0
		self._ollama = ollama

	def getMessage(self, id) -> dict:
		return self._chat.get(id, {})

	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		if len(self._chat) > 100:
			if self._chat.get(100, {}).get("role", "") != "system":
				oldest_id = min(self._chat.keys())
				self._chat.pop(oldest_id)
				self._last_msgid -= 1

		self._chat[self._last_msgid] = {"role": author, "content": msg, **optional}
		self._last_msgid += 1

	def getFirstMessage(self) -> dict:
		return self._chat.get(0, {})

	def getLastMessage(self) -> dict:
		if self._last_msgid == 0:
			return {}
		return self._chat.get(self._last_msgid - 1, {})

	def getRandomMessage(self) -> dict:
		return self._chat.get(random.choice(list(self._chat.keys())), {})
	
	def getChatHistory(self) -> list:
		return [self._chat[k] for k in sorted(self._chat.keys())]

	def RecallPartially(self, long_mem) -> None:
		memories = long_mem.getMessages()
		shorted_memories = {}
		for id, msg in memories.items():
			try:
				generated_msg = self._ollama.generate(self._model,
					"Shorten the message: \"{}\". Don't include any quotes.".format(msg["content"])
				)['response']
			except Exception as e:
				raise e
			shorted_memories[id] = {"role": msg["role"], "content": generated_msg}
		return shorted_memories