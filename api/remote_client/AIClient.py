import abc

class AIClient:
	@abc.abstractmethod
	def __init__(self, ip, port, ssl=False): pass

	@abc.abstractmethod
	def generate(self, model, prompt, system="", think=False, temperature=None, **kwargs): pass

	@abc.abstractmethod
	def chat(self, model, messages: list[dict], think=False, temperature=None, **kwargs): pass

	@abc.abstractmethod
	def loadModel(self, model): pass
	@abc.abstractmethod
	def unloadModel(self, model): pass

	@abc.abstractmethod
	def getModels(self): pass
	@abc.abstractmethod
	def getModelInfo(self, model): pass

	@abc.abstractmethod
	def getLoadedModels(self): pass