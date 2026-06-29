from api.bot.Bot import Bot
from api.bot.types.Alive import Alive
from api.bot.types.Creator import Creator
from api.bot.types.Dummy import Dummy
from api.personality.Generator import Generator
from api.personality.Person import Person
from api.utils.FileManager import FileManager
from api.Core import Core
import os

class BotManager:
	def __init__(self, core: Core):
		self._bots_list = {}
		self._last_id = 0
		self._main_bot = None
		self._core = core
		self._generator = Generator()

	def setMainBot(self, bot: Bot) -> None: self._main_bot = bot

	def getCore(self) -> Core: return self._core
	def getBots(self) -> dict: return self._bots_list
	def getMainBot(self) -> Bot | None: return self._main_bot
	def getBot(self, id) -> Bot | None: return self._bots_list.get(id, None)


	def _create(self, bot_class, model: str, *args, **kwargs) -> Bot:
		id = self._last_id
		bot = bot_class(model, id, self, *args, **kwargs)
		self._bots_list[id] = bot
		self._last_id += 1
		return bot


	def create_normal(self, model: str, ollama_client, fancy_mode: bool = False, max_long: int = 100) -> Bot:
		mode = "fancy" if fancy_mode else "normal"
		id = self._last_id

		person_file = FileManager(f"persons/{id}.json", 'json')

		if person_file.readFile():
			person = Generator.get_person(False, **person_file.readFile())
		else:
			person = self._generator.generate_use_ai(False, model, ollama_client)
			person_file.rewriteFile(person.get_summary())

		os.makedirs(f"bots/{id}/", exist_ok=True)
		file_man = FileManager(f"bots/{id}/long.json", 'json', max_long)
		return self._create(Bot, model, file_man, person, ollama_client, mode)


	def create_dummy(self, model: str, ollama_client, fancy_mode: bool = False, max_long: int = 100) -> Bot:
		mode = "fancy" if fancy_mode else "normal"
		id = self._last_id

		os.makedirs(f"bots/{id}/", exist_ok=True)
		file_man = FileManager(f"bots/{id}/long.json", 'json', max_long)
		return self._create(Dummy, model, file_man, ollama_client, mode)


	def create_alive(self, model: str, ollama_client, fancy_mode: bool = False, max_long: int = 100) -> Bot:
		mode = "fancy" if fancy_mode else "normal"
		id = self._last_id

		person_file = FileManager(f"persons/{id}.json", 'json')
		if person_file.readFile():
			person = Generator.get_person(False, **person_file.readFile())
		else:
			person = self._generator.generate_use_ai(False, model, ollama_client)
			person_file.rewriteFile(person.get_summary())

		os.makedirs(f"bots/{id}/", exist_ok=True)
		file_man = FileManager(f"bots/{id}/long.json", 'json', max_long)
		return self._create(Alive, model, file_man, person, ollama_client, mode)


	def create_author(self, model: str, ollama_client, fancy_mode: bool = False, max_long: int = 100) -> Bot:
		mode = "fancy" if fancy_mode else "normal"
		id = self._last_id

		person_file = FileManager(f"persons/{id}.json", 'json')

		if person_file.readFile():
			person = Generator.get_person(True, **person_file.readFile())
		else:
			person = self._generator.generate_use_ai(True, model, ollama_client)
			person_file.rewriteFile(person.get_summary())

		os.makedirs(f"bots/{id}/", exist_ok=True)
		file_man = FileManager(f"bots/{id}/long.json", 'json', max_long)
		return self._create(Creator, model, file_man, person, ollama_client, mode)