from api.ai_tools.ToolsManager import ToolsManager
from api.remote_client.OllamaClient import OllamaClient

class Think:
	def __init__(self, model: str, ollama: OllamaClient):
		self._model = model
		self._ollama = ollama

	def generate(self, prompt: str, tools_man: ToolsManager = None, **kwargs):
		if not tools_man:
			response = self._ollama.generate(self._model, prompt, think=True, **kwargs)
		else:
			response = self._ollama.gen_with_tools(self._model, prompt, think=True, tools_man=tools_man, **kwargs)
		return (response.thinking, response.response)

	def chat(self, chat: list, tools_man: ToolsManager = None, **kwargs):
		if not tools_man:
			response = self._ollama.chat(self._model, chat, think=True, **kwargs)
		else:
			response = self._ollama.chat_with_tools(self._model, chat, think=True, tools_man=tools_man, **kwargs)
		return (response.message.thinking, response.message.content)