import threading
import time

class ShTimer:
	def __init__(self, time: int, func, args):
		self._time = time
		self.func = func
		self.args = args

	def _tick(self):
		self.func(*self.args)
		t = threading.Timer(self._time, self._tick)
		t.start()

	def start(self):
		t = threading.Timer(self._time, self._tick)
		t.start()
