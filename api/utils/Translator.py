import os

os.environ["translators_default_region"] = "EN"
import translators as ts
from urllib3 import HTTPSConnectionPool
#from requests.

class Translator:
	def __init__(self, logger, target_language: str):
		self._logger = logger
		self._tl = target_language.lower()

	def translate(self, text):
		try:
			return ts.translate_text(text, translator="google", to_language=self._tl)
		except Exception as e:
			self._logger.error(str(e))
			return text