class IdeasMemory:
	def __init__(self, fileman):
		self._file = fileman

	def getMessage(self, id) -> dict:
		history = self._file.readFile()
		return history[id]

	def getMessages(self) -> dict:
		return self._file.readFile()

	def getLastId(self):
		return len(self.getChatHistory())

	def getChatHistory(self) -> list:
		return list(self.getMessages().values())

	def addIdea(self, msg: str, optional: dict = {}) -> None:
		data = {"role": "assistant", "content": msg, **optional}
		self._file.writeFile(self.getLastId(), data)

	def clear(self):
		self._file.rewriteFile({})
