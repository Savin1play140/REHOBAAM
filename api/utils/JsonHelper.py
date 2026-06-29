import json
import os

class JsonHelper:
	def __init__(self, filename):
		self._file = str(filename)
		if not os.path.exists(filename):
			file = open(self._file, 'w')
			file.write("{}")

	def read(self) -> dict:
		with open(self._file) as file:
			content = file.read()
			return json.loads(content)
	
	def write(self, id, data: dict):
		old_file = self.read()
		if str(id) in old_file:
			return
		old_file[id] = data
		with open(self._file, 'w') as file:
			file.write(json.dumps(old_file, indent=4))

	def rewrite(self, data: dict):
		with open(self._file, 'w') as file:
			file.write(json.dumps(data, indent=4))