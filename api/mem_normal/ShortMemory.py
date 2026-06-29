import random
from api.utils.Functions import GTTSCM_IH

class ShortMemory:
	def __init__(self):
		self._chat = {}
		self._last_msgid = 0

	def getMessage(self, id) -> dict:
		return self._chat.get(id, None)
	
	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		if len(self._chat) > 100:
			if (self._chat[100].get("role", "") != "system"):
				self._chat.popitem()
				self._last_msgid -= 1

		msg = {"role": author, "content": msg}
		self._chat[self._last_msgid] = {**msg, **optional}

		self._last_msgid += 1

	def getFirstMessage(self) -> dict:
		return self._chat.get(0, {})

	def getLastMessage(self) -> dict:
		return self._chat.get(self._last_msgid, {})

	def getRandomMessage(self) -> dict:
		return self._chat.get(random.randint(0, self._last_msgid), {})

	def getChatHistory(self) -> list:
		return list(self._chat.values())

	def RecallPartially(self, long_mem) -> None:
		shortest_mem = {"role": "None", "content": ""}
		memories = {}
		for id, shorted_mem in GTTSCM_IH(long_mem.getMessages()).items():
			memories[id] = shorted_mem

		if len(memories) > 0:
			self._chat = {**self._chat, **memories}