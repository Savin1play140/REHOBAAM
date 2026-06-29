import random
from api.utils.Functions import GTTSCM_IH
from api.remote_client.OllamaClient import OllamaClient

class ChatMemory:
	def __init__(self, model: str, ollama: OllamaClient):
		self._chat = {}
		self._model = model
		self._last_msgid = 0
		self._ollama = ollama

	def getMessage(self, id):
		return self._chat.get(id, None)
	
	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		self._chat[self._last_msgid] = {"role": author, "content": msg, **optional}
		self._last_msgid += 1

	def getLastMessage(self):
		if self._last_msgid == 0:
			return None
		return self._chat.get(self._last_msgid - 1, None)
	
	def getRandomMessage(self):
		if not self._chat:
			return None
		rand_id = random.choice(list(self._chat.keys()))
		return self._chat[rand_id]
	
	def getChatHistory(self) -> list:
		return [self._chat[k] for k in sorted(self._chat.keys())]

	def RecallPartially(self, long_mem):
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