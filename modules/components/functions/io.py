from typing import Self
from modules.logger import Logger
from modules.components.context import Module, Text

class IO(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		IO Module
		"""

		super().__init__("IO", logger)
		self.module_functions = [
			self.out,
			self.input
		]

		return None

	def out(self: Self, *args) -> None:
		"""
		Outputs its inputs in console
		"""

		data = [arg.to_text() for arg in args]
		self.logger.out(*data)

		return None
	
	def input(self: Self, *args) -> None:
		"""
		Takes inputs from console
		"""

		data = [arg.to_text() for arg in args]
		self.logger.out(*data, break_line=False)
		input_data = input()
		return_data = Text(None, input_data)

		return return_data

