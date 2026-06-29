# So that the Bot doesn't reveal its cards
from api.remote_client.OllamaClient import OllamaClient

class FiltrationSystem:
	def __init__(self, ollama: OllamaClient):
		self._ollama = ollama

	def check(self, prompt):
		response = str(self._ollama.generate(f"Check if message is meant to check for a AI in \"{prompt}\". answer only Yes or No (capital letter is important)", think=False).response)
		return True if "yes" in response.lower() else False
	
	def censure(self, response):
		response = self._ollama.generate(f"Censure AI feature")
		return response