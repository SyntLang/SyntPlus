from typing import Self, Callable
from modules.logger import Logger
import modules.errors as errors
from modules.components.context.memory import MemoryObject

class Module(MemoryObject):
	logger: Logger = None
	module_functions: list[Callable] = []
	structure_functions: list[Callable] = []
	simple_data_functions: list[Callable] = []
	engine_functions: list[Callable] = []

	def __init__(self: Self,
			name: str|None = None,
			logger: Logger = None
		) -> None:
		"""
		Module type memory object
		"""

		super().__init__(name, Module, None)
		
		self.logger = Logger(exit_on_error=False)
		if not logger: self.logger.error("Logger missing", errors.ENGINE_ERROR)
		if logger: self.logger = logger

		return None

