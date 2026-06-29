import abc

class Core:
	@abc.abstractmethod
	def getVersion(self) -> str: return "null"
	@abc.abstractmethod
	def getName(self) -> str: return "null"
	@abc.abstractmethod
	def getGUIManager(self): return self._gui
	@abc.abstractmethod
	def getBotManager(self): return self._bot_man
	@abc.abstractmethod
	def getEventManager(self): return self._events
	@abc.abstractmethod
	def getOllama(self): return self._ollama