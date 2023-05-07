from typing import Self
from modules.logger import Logger
from modules.components.context import MemoryObject, Module, Collection, Text
import modules.errors as errors
import sys

class System(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		System Module
		"""

		super().__init__("System", logger)
		self.module_functions = [
			(self.version, "version", "ver"),
			(self.info, "info", "help"),
			(self.end, "end", "exit", "quit")
		]
		self.engine_functions = [
			self.version
		]

		return None
	
	def version(self: Self, *args) -> Collection|None:
		"""
		Version of Engine
		"""

		engine = args[-1]
		if not engine:
			self.logger.error("Engine data inappropriate", errors.ENGINE_ERROR)
			return None

		return Collection(
			"Version",
			value = [Text(None, str(v)) for v in engine.version.values()],
			index = [Text(None, str(v)) for v in engine.version.keys()],
			connector = "."
		)
	
	def info(self: Self, *args) -> Collection|None:
		"""
		Gets help data(if exists) for object
		"""

		if len(args) < 1:
			self.logger.error("Need an object to get data", errors.ARG_MISSING_ERROR)
			return None

		alg = args[0]
		data = {
			"name": alg.name,
			"type": alg.type.__name__,
			"help": alg.help_data if hasattr(alg, "help_data") else None,
			"value": alg.value if not(callable(alg.value)) else alg.value.__name__
		}
		if data["type"].lower() == "collection":
			data["value"] = alg.to_text()

		return Collection(
			f"Help Data - {alg.name}",
			value = [MemoryObject(None, None, data[v]) for v in data if data[v]],
			index = [Text(None, v) for v in data if data[v]],
			connector = "\n"
		)
	
	def end(self: Self, *args) -> None:
		"""
		Ends the program
		"""

		sys.exit()

