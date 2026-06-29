from api.BotManager import BotManager
from api.ai_tools.ToolsManager import ToolsManager
from api.Core import Core
import os

class REHOBAAM(Core):
	def getVersion(self):
		return "v0.3-alpha13"
	def getName(self):
		return "R.E.H.O.B.A.A.M."

	def __init__(self):
		self.createDirs()
		self._bot_man = BotManager(self)

		self._started = False

		self._integrated = {}

		self._tools = ToolsManager()


	def getToolsMan(self) -> ToolsManager:
		return self._tools


	def integrate(self, integrate_name: str, integrate, **kwargs):
		self._integrated[integrate_name] = integrate(self, **kwargs)


	def start(self):
		self.createDirs()
		if self._started == True:
			raise Exception("Core has been started")

		self._started = True
		for name, integrate in self._integrated.items():
			integrate.start()

	def is_started(self) -> bool:
		return self._started


	def stop(self):
		if self._started == False:
			raise Exception("Core has been stopped or has not runned")

		self._started = False
		for name, integrate in self._integrated.items():
			integrate.stop()


	def createDirs(self):
		if not os.path.exists("bots/"): os.mkdir("bots/")
		#if not os.path.exists("logs/"): os.mkdir("logs/")
		if not os.path.exists("persons/"): os.mkdir("persons/")

	def getBotManager(self) -> BotManager: return self._bot_man