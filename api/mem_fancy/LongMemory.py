from api.remote_client.OllamaClient import OllamaClient

class LongMemory:
	def __init__(self, fileman, model: str, ollama: OllamaClient):
		self._file = fileman
		self._ollama = ollama
		self._model = model
		self._last_id = self._get_last_id()

	def _get_last_id(self):
		history = self._file.readFile()
		if not history:
			return 0
		return int(max(history.keys())) + 1

	def getMessage(self, id) -> dict:
		history = self._file.readFile()
		return history.get(id, None)

	def getMessages(self) -> dict:
		return self._file.readFile()

	def getChatHistory(self) -> list:
		return [msg for msg in self.getMessages().values()]

	def addMessage(self, author, msg: str, optional: dict = {}) -> None:
		try:
			shortened = self._ollama.generate(self._model, "Shorten this message: \"{}\". Don't include any quotes.".format(msg))
			content = shortened.response
		except Exception as e:
			raise e
		data = {"role": author, "content": content, **optional}
		self._file.writeFile(self._last_id, data)
		self._last_id += 1

	def clear(self):
		self._file.rewriteFile({})
		self._last_id = 0

	def Remember(self, short_mem):
		for msg in short_mem.getChatHistory():
			try:
				shortened_mem = self._ollama.generate(self._model, 
					"Reduce the amount of this message: \"{}\". Don't include any quotes.".format(msg['content'])
				)['response']
			except Exception as e:
				raise e
			self._file.writeFile(self._last_id, {"role": msg['role'], "content": shortened_mem})
			self._last_id += 1