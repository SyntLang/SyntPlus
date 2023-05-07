from typing import Self, Callable
from modules.components.context.memory import MemoryObject
from modules.components.context.void import Void

class Structure(MemoryObject):
	task: Callable|str|None = None
	help_data: str = ""

	def __init__(self: Self,
			name: str|None = None,
			task: str|None = None,
			help_data: str = "",
		) -> None:
		"""
		Structure type memory object
		"""

		super().__init__(name, Structure, task)
		self.task = task
		self.help_data = help_data.strip()

		return None

	def run(self: Self, engine = None, code: list = [], run_data: list = []) -> Void:
		"""
		Run structure
		"""

		if not self.task: return Void()
		if callable(self.task):
			self.task(engine, code, run_data)

			return Void()
		
		iterated_code = engine.iterator.iterate(self.task)
		engine.run(iterated_code)

		return Void()
	
	def to_text(self: Self) -> str:
		return self.name if self.name else ""

