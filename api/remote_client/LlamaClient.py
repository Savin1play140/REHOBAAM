from openai import OpenAI
from api.remote_client.AIClient import AIClient

class LlamaClient(AIClient):
	def __init__(self, ip, port, ssl=False):
		self._client = OpenAI(
			base_url=f"http{"s" if ssl else ""}://{ip}:{str(port)}/v1", # e.g., "http://192.168.1.100:8000/v1"
			api_key="none" # llama.cpp server typically doesn't require a key
		)

	def generate(self, model, prompt, system="", think=False, temperature=None, **kwargs):
		temp_history = [
			{"role": "user", "content": prompt}
		]
		if system!= "":
			temp_history.append({"role": "system", "content": system})
		response = client.chat.completions.create(
			model="default", # or the model alias you used on server
			messages=temp_history,
			stream=False
		)

		return response.choices[0].message.content


	def chat(self, model, messages: list[dict], think=False, temperature=None, **kwargs):
		response = client.chat.completions.create(
			model="default", # or the model alias you used on server
			messages=messages,
			stream=False
		)
		return response.choices[0]

	def loadModel(self, model): pass
	def unloadModel(self, model): pass

	def getModels(self): pass
	def getModelInfo(self, model): pass

	def getLoadedModels(self): pass