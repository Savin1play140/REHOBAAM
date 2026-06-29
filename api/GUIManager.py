from api.gui.Console import Console
from api.utils.Functions import set_console_title
from api.Integrable import Integrable

class GUIManager(Integrable):
	def __init__(self, core, translate_lang, mode='console', bot = None):
		super().__init__(core)
		self._core = core
		self._logger = core.getLogger()
		self._title = core.getName()+" "+core.getVersion()
		set_console_title(self._title)
		self._stopped = False
		self._mode = mode
		self._tl = translate_lang
		self._bot = bot
		self._gui = None


	def start(self, core) -> None:
		if self._mode == 'console':
			self._gui = Console(self._logger, self._title, self._tl, self._bot)
		else:
			raise ValueError(f"Unknown GUI mode: {self._mode}")
		self._gui.run()

	def setBot(self, bot):
		self._bot = bot
		#self._gui.setBot(bot)

	def getInterface(self):
		return self._gui

	def stop(self, core):
		if self._stopped:
			return
		if self._gui:
			self._gui.stop()
		self._stopped = True

	def get_name(self) -> str:
		return "UI"
