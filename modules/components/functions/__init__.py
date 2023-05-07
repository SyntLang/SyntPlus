from typing import Self, Callable
from modules.logger import Logger
import modules.errors as errors
from modules.components.context import Module, Algorithm, Structure
from modules.components.functions.comments import Comments
from modules.components.functions.io import IO
from modules.components.functions.variables import Variable
from modules.components.functions.system import System
from modules.components.functions.operations import Operations
from modules.components.functions.maths import Maths
from modules.components.functions.loops import Loops
from modules.components.functions.logic import Logic

class Modules:
	activated_modules: list[Module] = []
	functions: list[Callable] = []
	structure_functions: list[Callable] = []
	simple_data_functions: list[Callable] = []
	engine_functions: list[Callable] = []
	algorithms: dict[str, Algorithm] = {}

	logger: Logger = None

	def __init__(self: Self, modules: list = [], logger: Logger = None) -> None:
		"""
		All Module
		"""

		self.logger = Logger(exit_on_error=False)
		if not logger: self.logger.error("Logger missing", errors.ENGINE_ERROR)
		if logger: self.logger = logger

		for module in modules:
			self.activated_modules.append(module(logger))
		
		self.get_active_functions()
		self.get_structure_functions()
		self.get_algorithms()
		self.get_structures()

		return None
	
	def get_active_functions(self: Self) -> None:
		"""
		Gets a list of Callables
		"""

		for module in self.activated_modules:
			self.functions.extend(module.module_functions)
			self.simple_data_functions.extend(module.simple_data_functions)
			self.engine_functions.extend(module.engine_functions)

		return None
	
	def get_algorithms(self: Self) -> None:
		"""
		Gets a dictionary of all Algorithms
		"""

		for __func__ in self.functions:
			func = None
			alg_name = ""
			aliases = []
			
			if callable(__func__):
				func = __func__
				alg_name = func.__name__
			elif isinstance(__func__, (tuple, list)):
				func = __func__[0]
				
				if len(__func__) > 1: alg_name = __func__[1]
				if len(__func__) > 2: aliases = __func__[1:]

				if isinstance(func, str):
					for alias in [__func__[1]] + list(aliases):
						alg = {
							alias: Algorithm(
								name = None,
								code = func
							)
						}

						self.algorithms.update(alg)

					continue

			alg = {
				alg_name: Algorithm(
					name = func.__name__,
					code = func,
					help_data = func.__doc__,
					rich_data = func not in self.simple_data_functions,
					need_engine = func in self.engine_functions
				)
			}

			self.algorithms.update(alg)
			
			for alias in aliases:
				alg = {
					alias: Algorithm(
						name = func.__name__,
						code = func,
						help_data = func.__doc__,
						rich_data = func not in self.simple_data_functions,
						need_engine = func in self.engine_functions
					)
				}

				self.algorithms.update(alg)

		return None
	
	def get_structure_functions(self: Self) -> None:
		"""
		Gets a list of Callables
		"""

		for module in self.activated_modules:
			self.structure_functions.extend(module.structure_functions)

		return None
	
	def get_structures(self: Self) -> None:
		"""
		Gets a dictionary of all Structures
		"""

		for __func__ in self.structure_functions:
			func = None
			struc_name = ""
			aliases = []
			
			if callable(__func__):
				func = __func__
				struc_name = func.__name__
			elif isinstance(__func__, (tuple, list)):
				func = __func__[0]
				
				if len(__func__) > 1: struc_name = __func__[1]
				if len(__func__) > 2: aliases = __func__[1:]
			
				if isinstance(func, str):
					for alias in [__func__[1]] + list(aliases):
						struc = {
							alias: Structure(
								name = None,
								task = func
							)
						}

						self.algorithms.update(struc)

					continue

			struc = {
				struc_name: Structure(
					name = func.__name__,
					task = func,
					help_data = func.__doc__
				)
			}

			self.algorithms.update(struc)
			
			for alias in aliases:
				struc = {
					alias: Structure(
						name = func.__name__,
						task = func,
						help_data = func.__doc__
					)
				}

				self.algorithms.update(struc)

		return None

