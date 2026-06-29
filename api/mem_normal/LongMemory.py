class LongMemory:
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

	def addToLastId(self):
		self._last_id += 1

	def getChatHistory(self) -> list:
		return list(self.getMessages().values())

	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		data = {"role": author, "content": msg, **optional}
		self._file.writeFile(self.getLastId(), data)
		self.addToLastId()

	def clear(self):
		self._file.rewriteFile({})
		self._last_id = 0

	def Remember(self, short_mem):
		for msg in short_mem.getChatHistory():
			self.addMessage(msg["role"], msg["content"])