from typing import Self
from modules.logger import Logger
from modules.iterator import Iterator
from modules.components.context import (
	MemoryObject,
	Algorithm,
	Text,
	Number,
	Decimal,
	Binary,
	Void,
	Structure
)
import modules.errors as errors

class Runtime:
	version: dict = {}

	logger: Logger = None
	iterator: Iterator = None
	
	memory: dict[str, any] = {}
	alg_cache: list = []

	def __init__(self: Self, logger: Logger = None, iterator: Iterator = None) -> None:
		"""
		Runtime for Esolang
		"""

		self.logger = Logger(exit_on_error=False)
		if not logger: self.logger.error("Logger missing", errors.ENGINE_ERROR)
		if not iterator: self.logger.error("Iterator missing", errors.ENGINE_ERROR)
		if logger: self.logger = logger
		if iterator: self.iterator = iterator

		return None
	
	def push_to_memory(self: Self, data: dict = {}) -> None:
		"""
		Pushes algs into runtime memory
		"""

		self.memory.update(data)
		return None
	
	def run(self: Self, chunks: list = []) -> None:
		"""
		Executes code chunks
		"""

		if not chunks: return None
		current_cache = len(self.alg_cache)

		for chunk in chunks:
			if len(self.alg_cache) < current_cache: break
			if type(chunk) == list: self.run_chunk(chunk); continue
			if "(" in chunk: self.run_chunk([chunk, []]); continue

			if chunk in self.memory:
				chunk_object = self.memory[chunk]
				formatted_object = f"--- {chunk_object.name} ---\n"
				formatted_object += f"TYPE: {chunk_object.type.__name__}\n"
				
				if chunk_object.type != Algorithm:
					formatted_object += f"VALUE: {chunk_object.value}"
				else:
					formatted_object += f"DESCRIPTION: {chunk_object.help_data}"
				
				continue
			
			error_msg = f"Unknown object/algorithm: {chunk}"
			self.logger.error(error_msg, errors.UNDEF_ANY_ERROR)

		return None
	
	def run_chunk(self: Self, chunk: list = []) -> None:
		"""
		Executes one chunk of code
		"""

		if not chunk: return None

		chunk_primary_data, chunk_args = chunk
		chunk_data = self.get_primary_data(chunk_primary_data)

		if not chunk_data[0]: return None

		save_data = self.run_algorithm(chunk_data, chunk_args)
		if len(chunk_data) > 2 and not save_data.name == "--structure-void--":
			self.memory[chunk_data[2]] = save_data

		return save_data
	
	def parse_arg(self: Self, arg: any = None) -> None|MemoryObject:
		"""
		Parse Argument Type
		"""

		if isinstance(arg, type(None)): return None

		if any([str(arg).startswith("\'"), str(arg).startswith("\"")]):
			if str(arg).endswith("\""):
				arg_object = Text(None, str(arg)[1:-1])
			else:
				arg_object = Text(None, str(arg)[1:])
			
			return arg_object

		if all([ch in "-0123456789.," for ch in str(arg)]):
			if str(arg).count("-") <= 1:
				if (str(arg).startswith("-") if "-" in arg else True):
					if all([ch in "-0123456789," for ch in str(arg)]):
						arg_object = Number(None, int("0" + str(arg).replace(",", "")))
						return arg_object

					if str(arg).count(".") == 1:
						arg_object = Decimal(None, float("0" + str(arg).replace(",", "")))
						return arg_object

		if str(arg).upper() in ["TRUE", "FALSE", "ON", "OFF"]:
			arg_object = Binary(None, True if str(arg).upper() in ["TRUE", "ON"] else False)
			return arg_object

		if arg in ["VOID", "NONE", "NOTHING", "EMPTY"]:
			arg_object = Void(None)
			return arg_object
		
		return None
	
	def evaluate_args(self: Self, args: list = [], *,
			no_var = False
		) -> list:
		"""
		Evaluates the value of arguments passed
		"""

		if not args: return []
		evaluated_args = []
		for arg in args:
			if type(arg) == list:
				alg_data = self.get_primary_data(arg[0])
				if alg_data[0] and alg_data[1] in self.memory:
					data = self.run_chunk(arg)
					evaluated_args.append(data)
					continue

				self.logger.error(f"Undefined algorithm: {alg_data[1]}", errors.UNDEF_ALG_ERROR)
				continue
			
			if not no_var and (arg in self.memory): evaluated_args.append(self.memory[arg]); continue
			
			arg_object = self.parse_arg(arg)
			if not isinstance(arg_object, type(None)):
				evaluated_args.append(arg_object)
				continue

			if "(" in str(arg):
				alg_data = self.get_primary_data(arg)
				if alg_data[0] and alg_data[1] in self.memory:
					evaluated_args.append([arg, []])
					continue

			if not no_var:
				self.logger.error(f"Undefined value: {arg}", errors.UNDEF_ANY_ERROR)
				continue
			
			arg_object = self.parse_arg(f"\"{arg}")
			evaluated_args.append(arg_object)

		return evaluated_args
	
	def check_alg_exists(self: Self, alg_name: str = None) -> bool:
		"""
		Checks if an algorithm exists
		"""

		if not alg_name:
			self.logger.error("Algorithm name is required to run it", errors.ENGINE_ERROR)
			return False
		
		if alg_name not in self.memory:
			self.logger.error(f"Undefined algorithm: {alg_name}", errors.UNDEF_ALG_ERROR)
			return False
		
		if self.memory[alg_name].type == Structure:
			return 2
		
		if (obj := self.memory[alg_name]).type != Algorithm:
			err_data = f"{alg_name} is not an algorithm, but {obj.type.__name__}"
			self.logger.error(err_data, errors.UNDEF_ALG_ERROR)
			return False

		return 1
	
	def get_primary_data(self: Self, data: str = None) -> list:
		"""
		Gets data about the chunk from its first line
		"""

		alg_name = data.split("(")[0]
		alg_deviation = self.check_alg_exists(alg_name)

		if not alg_deviation: return [False, data]
		
		store_value = ""
		if len(st_val := data.split("(")) > 1: store_value = st_val[1].split(")")[0]

		output = [alg_deviation, alg_name]
		if store_value: output += [store_value]

		return output
	
	def run_algorithm(self: Self,
			alg_data: list = [],
			raw_args: list[any] = [],
		) -> any:
		"""
		Runs a function
		"""

		alg_name = alg_data[1]
		if not self.check_alg_exists(alg_name): return None
		
		self.alg_cache.append(alg_data)
		alg: Algorithm|Structure = self.memory[alg_name]

		if alg.type == Algorithm:
			evaluated_args = self.evaluate_args(raw_args)
			return_object = alg.run(evaluated_args, engine=self)
			del self.alg_cache[-1]

			return return_object
		
		prev_cache_length = len(self.alg_cache)
		alg.run(self, raw_args, alg_data[1:])
		if prev_cache_length == len(self.alg_cache): del self.alg_cache[-1]

		return Void("--structure-void--")

