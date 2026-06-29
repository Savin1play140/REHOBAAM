class MemoryManager:
	def __init__(self, fileman, model: str, ollama_client, mode: str = "normal"):
		if mode == 'normal':
			from api.mem_normal.LongMemory import LongMemory
			from api.mem_normal.ShortMemory import ShortMemory
			from api.mem_normal.ChatMemory import ChatMemory
			from api.mem_normal.ContextMemory import ContextMemory

			self._long = LongMemory(fileman)
			self._short = ShortMemory()
			self._chat = ChatMemory()
			self._context = ContextMemory(fileman)

		elif mode == 'fancy':
			from api.mem_fancy.LongMemory import LongMemory
			from api.mem_fancy.ShortMemory import ShortMemory
			from api.mem_fancy.ChatMemory import ChatMemory
			from api.mem_fancy.ContextMemory import ContextMemory

			self._long = LongMemory(fileman, model, ollama_client)
			self._short = ShortMemory(model, ollama_client)
			self._chat = ChatMemory(model, ollama_client)
			self._context = ContextMemory(fileman)

		else:
			raise ValueError(f"Unknown memory mode: {mode}")

	def getLong(self): return self._long
	def getShort(self): return self._short
	def getChat(self): return self._chat
	def getContext(self): return self._context

	def addMessage(self, author: str, msg: str):
		self._chat.addMessage(author, msg)
		self._short.addMessage(author, msg)
		self._long.addMessage(author, msg)