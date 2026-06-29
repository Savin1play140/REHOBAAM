from typing import Iterable

import ollama
from api.remote_client.AIClient import AIClient
from api.ai_tools.ToolsManager import ToolsManager

class OllamaClient(AIClient):
	def __init__(self, ip, port, ssl=False):
		self.base_url = f'http{"s" if ssl else ""}://{ip}:{port}'
		self._client = ollama.Client(self.base_url)


	def generate(self, model, prompt, system="", think=False, temperature=None, **kwargs):
		params = {"system": system, "think": think, "options": {}}

		if temperature:
			params["options"]["temperature"] = temperature
		params.update(kwargs)


		return self._client.generate(model, prompt, **params)


	def gen_with_tools(self, model: str, prompt: str, tools_man: ToolsManager, think: bool = False, temperature: float = None, **kwargs):
		params = {"think": think, "options": {}}

		if temperature:
			params["options"]["temperature"] = temperature
		params.update(kwargs)

		messages = [{"role": "user", "content": prompt}]

		res = self._client.chat(model, messages, tools=tools_man.get_tools_list(), think=think)

		if res.message.tool_calls:
			for call in res.message.tool_calls:
				tool = tools_man.get_tool(call.function.name)
				if not tool:
					messages.append({"role": "system", "content": f"Tool {call.function.name} not found or not exists!"})
					continue

				result = (tool)(**call.function.arguments)
				print(f"Called {call.function.name}({call.function.arguments}). output: {result}")
				messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})
		else:
			messages.append(res.message)

		return self._client.chat(model, messages, **params).message


	def chat(self, model, messages: list[dict], think=False, temperature=None, **kwargs):
		params = {"think": think, "options": {}}

		if temperature:
			params["options"]["temperature"] = temperature
		params.update(kwargs)

		data = self._client.chat(model, messages, **params)

		return data


	def tools_call(self, calls: Iterable, tools_man: ToolsManager):
		messages = []
		for call in calls:
			tool = tools_man.get_tool(call.function.name)
			if not tool:
				messages.append({"role": "system", "content": f"Tool {call.function.name} not found or not exists!"})
				continue

			result = (tool)(**call.function.arguments)
			print(f"Called {call.function.name}({call.function.arguments}). output: {result}")
			messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

		return messages


	def chat_with_tools(self, model: str, messages: list[dict[str, str]], tools_man: ToolsManager, think: bool = False, temperature: float = None, **kwargs):
		params = {"think": think, "options": {}}

		if temperature:
			params["options"]["temperature"] = temperature
		params.update(kwargs)

		res = self._client.chat(model, messages, tools=tools_man.get_tools_list(), think=think)
		messages.append(res.message)
		print(tools_man.get_tools_list())

		tools_called = res.message.tool_calls is not None
		while tools_called:
			try:
				messages.extend(self.tools_call(res.message.tool_calls, tools_man))
			except Exception as e:
				print(e)
				messages.append({"role": "tool", "tool_name": "sys_logger", "content": str(e)})
			except TypeError as e:
				print(e)
				messages.append({"role": "tool", "tool_name": "sys_logger", "content": str(e)})

			res = self._client.chat(model, messages, tools=tools_man.get_tools_list(), think=think)
			messages.append(res.message)
			tools_called = res.message.tool_calls is not None

		if res.message.content == "":
			res = self._client.chat(model, messages, **params)
		return res


	def loadModel(self, model): return self._client.generate(model)
	def unloadModel(self, model): return self._client.generate(model, keep_alive=0)

	def getModels(self): return self._client.list()
	def getModelInfo(self, model): return self._client.show(model)
	# def getVersion(self): return self._client.
	def getLoadedModels(self): return self._client.ps()

