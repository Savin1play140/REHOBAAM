import threading
import time
import random

class RandTimer:
	def __init__(self, min_time: int, max_time: int, func, args):
		self._time = (min_time, max_time)
		self.func = func
		self.args = args

	def _tick(self):
		self.func(*self.args)
		t = threading.Timer(random.randint(*self._time), self._tick)
		t.start()

	def start(self):
		t = threading.Timer(random.randint(*self._time), self._tick)
		t.start()
