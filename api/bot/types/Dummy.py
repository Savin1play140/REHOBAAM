from api.ai_tools.ToolsManager import ToolsManager
from api.bot.Bot import Bot
from api.bot.think.NoThink import NoThink
from api.utils.FileManager import FileManager
from api.personality.Person import Person
from api.remote_client.OllamaClient import OllamaClient
from api.bot.MemoryManager import MemoryManager
from api.utils.Functions import system_prompt

class Dummy(Bot):
	def __init__(self,
			model: str, id, manager,
			fileman: FileManager,
			ollama_client: OllamaClient, mode: str = "normal"):
		self._manager = manager
		self._core = manager.getCore()
		self._id = id
		self._model = model

		self._mem = MemoryManager(fileman, model, ollama_client, mode)
		self._mem.getShort().RecallPartially(self._mem.getLong())
		self._mem.getShort().addMessage("system", "")
		self._no_think = NoThink(model, ollama_client)


	def _send(self, author: str, message: str, tools_man: ToolsManager = None):
		user_clear = f""""""

		if self._protection.CBQ_alt(message):
			_, re_input = self._no_think.generate(message, system=user_clear, think=False)

			return self._send(author, re_input)
		self._mem.addMessage(author, message)

		_, response = self._no_think.chat(self._mem.getShort().getChatHistory(), options={'temperature': 0.1}, tools_man=tools_man, think=False)

		response = {"role": "assistant", "content": response}

		#self._core.getEventManager().emit("bot_send", self._id, response)
		self._mem.addMessage(response["role"], response.get('content', ""))

		return response.get('content', "")

	def sendMessage(self, msg: str, role: str = "user", tools_man: ToolsManager = None) -> str:
		return self._send(role, msg, tools_man=tools_man)
