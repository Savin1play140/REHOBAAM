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

class Creator(Bot):
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

		ideas_fileman = FileManager(f'bots/{id}/ideas.{"json" if fileman.getFileMode() == "json" else "txt"}', fileman.getFileMode(), -1)

		if mode == "normal":
			from api.mem_normal.IdeasMemory import IdeasMemory
			self._ideas = IdeasMemory(ideas_fileman)
		elif mode == "fancy":
			from api.mem_fancy.IdeasMemory import IdeasMemory
			self._ideas = IdeasMemory(ideas_fileman)
		else:
			raise ValueError(f"Unknown memory mode: {mode}")

	def _send(self, author: str, message: str, tools_man: ToolsManager = None) -> str:
		user_clear = f""""""

		if self._protection.CBQ_alt(message):
			_, re_input = self._think.generate(message, system=user_clear)

			return self._send(author, re_input)
		self._mem.addMessage(author, message)

		_, response = self._think.chat(self._mem.getShort().getChatHistory(), tools_man=tools_man, options={"temperature": 0.7})

		response = {"role": "assistant", "content": response}

		#self._core.getEventManager().emit("bot_send", self._id, response)
		self._mem.addMessage(response["role"], response.get('content', ""))

		return response.get('content', "")

	def sendMessage(self, msg: str, role: str = "user", tools_man: ToolsManager = None) -> str:
		return self._send(role, msg, tools_man=tools_man)

	def generate_idea(self, theme: str, size: str = "normal", addotional: str = "Write from your character's perspective.", tools_man: ToolsManager = None) -> tuple:
		system = f"""You are {str(self._person)}"""
		prompt= f"""{system}.
Like {self._person.get_firstname()} should you come up with an idea for a topic {theme} from the perspective of {self._person.get_firstname()}.
{addotional}"""
		think, response = "", ""

		if size == "low":
			think, response = self._no_think.generate(prompt)

		elif size == "normal":
			think, response = self._think.generate(prompt)

		elif size == "high":
			think, response = self._deep_think.generate(prompt)

		else:
			raise Exception(f"unavailable idea size: {size}. must be a lowz normal or high")

		self._ideas.addIdea(response)
		return (think, response)
