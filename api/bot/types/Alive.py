from api.ai_tools.ToolsManager import ToolsManager
from api.bot.Bot import Bot
from api.bot.system.Protection import Protection
from api.bot.think.DeepThink import DeepThink
from api.bot.think.NoThink import NoThink
from api.bot.think.Think import Think
from api.utils.FileManager import FileManager
from api.personality.Person import Person
from api.remote_client.OllamaClient import OllamaClient
from api.bot.MemoryManager import MemoryManager
from api.utils.Functions import system_prompt

class Alive(Bot):
	def __init__(self,
			model: str, id, manager,
			fileman: FileManager, person: Person,
			ollama_client: OllamaClient, mode: str = "normal"):
		self._manager = manager
		self._core = manager.getCore()
		self._id = id
		self._model = model
		self._person = person

		self._mem = MemoryManager(fileman, model, ollama_client, mode)
		self._mem.getShort().RecallPartially(self._mem.getLong())
		self._mem.getShort().addMessage("system", system_prompt(self._person))
		self._no_think = NoThink(model, ollama_client)
		self._think = Think(model, ollama_client)
		self._deep_think = DeepThink(model, ollama_client)
		self._protection = Protection(ollama_client, model)


	def _send(self, author: str, message: str, tools_man: ToolsManager = None):
		user_clear = f""""""

		self._logger.info(f"[{self._id}] {message}")

		if self._protection.CBQ_alt(message):
			_, re_input = self._think.generate(message, system=user_clear)

			return self._send(author, re_input)
		self._mem.addMessage(author, message)

		_, response = self._think.chat(self._mem.getShort().getChatHistory(), options={"temperature": 0.3}, tools_man=tools_man)

		response = {"role": "assistant", "content": response}

		#self._core.getEventManager().emit("bot_send", self._id, response)
		self._mem.addMessage(response["role"], response.get('content', ""))

		return response.get('content', "")

	def sendMessage(self, msg: str, role: str = "user", tools_man: ToolsManager = None) -> str:
		return self._send(role, msg, tools_man=tools_man)