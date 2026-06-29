from api.ai_tools.ToolsManager import ToolsManager
from api.bot.think.Think import Think
from api.remote_client.OllamaClient import OllamaClient


class DeepThink(Think):
	def __init__(self, model: str, ollama: OllamaClient):
		self._model = model
		self._ollama = ollama

	def generate(self, prompt: str, reducing: bool = True, tools_man: ToolsManager = None, **kwargs):
		response0 = self._ollama.generate(self._model, "Generate plan for \""+prompt+"\" ACCURACY: 100%", think=True)

		if not tools_man:
			response1 = self._ollama.generate(self._model, "Solve the problem according to plan: \""+response0["response"]+"\"", think=True, **kwargs)
		else:
			response1 = self._ollama.gen_with_tools(self._model, "Solve the problem according to plan: \""+response0["response"]+"\"", think=True, tools_man=tools_man, **kwargs)

		if reducing:
			response2 = self._ollama.generate(self._model, f"reduce the text to 400 symbols: {response1.response}", think=True, options={"temperature": 0.1})
			return (response1.thinking,response2.response)

		return (response1.thinking, response1.response)

	def chat(self, chat: list, reducing: bool = True, tools_man: ToolsManager = None, **kwargs):
		response0 = self._ollama.generate(self._model, "Generate plan for "+str(chat[len(chat)-1]), think=True, options={"temperature": 0.5})

		if not tools_man:
			response1 = self._ollama.chat(self._model, "Compile the plan: \""+response0["response"]+"\"", think=True, **kwargs)
		else:
			response1 = self._ollama.chat(self._model, "Compile the plan: \""+response0["response"]+"\"", think=True, tools_man=tools_man, **kwargs)

		if reducing:
			response2 = self._ollama.generate(self._model, f"reduce the text to 400 symbols: {response1.message.content}", think=True, options={"temperature": 0.1})
			return (response1.message.thinking, response2.response)

		return (response1.message.thinking, response1.message.content)