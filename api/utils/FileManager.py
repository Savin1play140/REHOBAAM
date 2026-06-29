from api.utils.JsonHelper import JsonHelper
from api.utils.RawHelper import RawHelper

class FileManager:
	def __init__(self, filename, filemode, max_size=100):
		self._filename = filename
		self._helper = None
		self._mode = filemode # json or raw
		self._max_size = max_size
		if self._mode == "json":
			self._helper = JsonHelper(filename)
		elif self._mode == "raw":
			self._helper = RawHelper(filename)
		else:
			raise ValueError(f"Unknown file mode: {self._mode}")


		self._datas = {}
		
	def getFileMode(self) -> str:
		return self._mode

	def readFile(self) -> dict:
		return self._helper.read()
	
	def writeFile(self, id, data):
		if self._max_size != -1 and len(self._datas) >= self._max_size:
			self._datas.popitem()
			self._datas[id] = data
			self._helper.rewrite(self._datas)
		else:
			self._helper.write(id, data)
			self._datas[id] = data

	def rewriteFile(self, data):
		self._helper.rewrite(data)
		self._datas = data