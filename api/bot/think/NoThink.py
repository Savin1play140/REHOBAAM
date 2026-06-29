from api.ai_tools.ToolsManager import ToolsManager
from api.remote_client.OllamaClient import OllamaClient

class NoThink:
	def __init__(self, model: str, ollama: OllamaClient):
		self._ollama = ollama
		self._model = model

	def generate(self, prompt: str, tools_man: ToolsManager = None, **kwargs):
		if not tools_man:
			response = self._ollama.generate(self._model, prompt, think=False, **kwargs)
		else:
			response = self._ollama.gen_with_tools(self._model, prompt, think=False, tools_man=tools_man, **kwargs)
		return ("", response.response)
	
	def chat(self, chat: list, tools_man: ToolsManager = None, **kwargs):
		if not tools_man:
			response = self._ollama.chat(self._model, chat, think=False, **kwargs)
		else:
			response = self._ollama.chat_with_tools(self._model, chat, think=False, tools_man=tools_man, **kwargs)
		return ("", response.message.content)