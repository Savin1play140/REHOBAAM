import random
from api.utils.Functions import GTTSCM_IH

class ChatMemory:
	def __init__(self):
		self._chat = {}
		self._last_msgid = 0

	def getMessage(self, id):
		return self._chat.get(id, None)
	
	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		self._chat[self._last_msgid] = {"role": author, "content": msg, **optional}
		self._last_msgid += 1

	def getLastMessage(self):
		return self._chat[self._last_msgid]
	
	def getRandomMessage(self):
		return self._chat[random.randint(0, self._last_msgid)]
	
	def getChatHistory(self) -> list:
		return list(self._chat.values())

	def RecallPartially(self, long_mem):
		shortest_mem = {"role": "None", "content": ""}
		memories = {}
		for id, shorted_mem in GTTSCM_IH(long_mem.getMessages()).items():
			memories[id] = shorted_mem

		if len(memories) > 0:
			self._chat = {**self._chat, **memories}