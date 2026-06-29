class ContextMemory:
	def __init__(self, fileman):
		self._file = fileman
		self._last_id = 0

	def getMessage(self, id) -> dict:
		history = self._file.readFile()
		return history[id]

	def getMessages(self) -> dict:
		return self._file.readFile()

	def getLastId(self):
		last_id = 0
		for msg in self.getChatHistory():
			last_id += 1
		return last_id

	def getChatHistory(self) -> list:
		return list(self.getMessages().values())

	def addIdea(self, msg: str, optional: dict = {}) -> None:
		data = {"role": "assistant", "content": msg, **optional}
		self._file.writeFile(self.getLastId(), data)
		self.addToLastId()

	def clear(self):
		self._file.rewriteFile({})
		self._last_id = 0
