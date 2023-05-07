from typing import Self
from modules.logger import Logger
from modules.components.context import Module

class Comments(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Comments Module
		"""

		super().__init__("Comments", logger)
		self.structure_functions = [
			(self.ignore, "ignore", "?", "...", "$", ">>>", "comment")
		]

		return None

	def ignore(self: Self, engine, code: list, run_data: list) -> None:
		"""
		Stops the current algorithm/structure process to continue
		"""

		return None

