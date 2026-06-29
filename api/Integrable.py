from api.Core import Core
import abc

class Integrable():
	@abc.abstractmethod
	def __init__(self, core: Core):
		...

	@abc.abstractmethod
	def start(self) -> None:
		...

	@abc.abstractmethod
	def stop(self) -> None:
		...

	@abc.abstractmethod
	def get_name(self) -> str:
		return "IT'S CANT USED AS REALLY INTEGRATE"