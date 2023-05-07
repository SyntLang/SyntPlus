from typing import Self
from modules.logger import Logger
from modules.components.context import Module, Number
import modules.errors as errors

class Loops(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Loops Module
		"""

		super().__init__("Loops", logger)
		self.structure_functions = [
			self.withdraw,
			self.repeat,
			self.forever
		]

		return None

	def withdraw(self: Self, engine, code: list, run_data: list) -> None:
		"""
		Stops the current algorithm/structure process to continue
		"""

		args = run_data[1:]
		eval_args = []
		exit_count = 1
		
		if len(args):
			args = args[0].replace(", ", ",")
			args = args.split(",")
			eval_args = engine.evaluate_args(args, no_var = True)
			exit_count = eval_args[0].to_number()
		
		if exit_count < 0:
			self.logger.error("Proccess Level can not be negative", errors.OUT_OF_BOUND_ERROR)
			return None
		
		if len(engine.alg_cache) - 1 < exit_count:
			self.logger.error("Can not exit from non existent process", errors.OUT_OF_BOUND_ERROR)
			return None
		
		for exit_itr in range(exit_count + 1):
			del engine.alg_cache[-1]
		
		return None
	
	def repeat(self: Self, engine, code: list, run_data: list) -> None:
		"""
		A loop that repeats code given amount of times
		"""

		repeat_level = len(engine.alg_cache)
		args = run_data[1:]
		eval_args = []
		
		if not len(args):
			while len(engine.alg_cache) >= repeat_level:
				engine.run(code)
			return None
		
		args = args[0].replace(", ", ",")
		args = args.split(",")
		eval_args = engine.evaluate_args(args, no_var = True)
		amount = eval_args[0].to_number()
		itr_index_var = None
		old_var_value = None
		
		if len(eval_args) > 1:
			itr_index_var = eval_args[1].to_text()
			if itr_index_var in engine.memory:
				old_var_value = engine.memory[itr_index_var]

		for itr_index in range(amount):
			if len(engine.alg_cache) < repeat_level: break
			if not isinstance(itr_index_var, type(None)):
				engine.memory[itr_index_var] = Number(itr_index_var, itr_index)
			
			engine.run(code)
		
		if not isinstance(old_var_value, type(None)):
			engine.memory[itr_index_var] = old_var_value

		return None
	
	def forever(self: Self, engine, code: list, run_data: list) -> None:
		"""
		A loop that repeats code forever
		"""

		repeat_level = len(engine.alg_cache)
		args = run_data[1:]
		eval_args = []
		
		if not len(args):
			while len(engine.alg_cache) >= repeat_level:
				engine.run(code)
			return None
		
		args = args[0].replace(", ", ",")
		args = args.split(",")
		eval_args = engine.evaluate_args(args, no_var = True)
		
		itr_index_var = None
		old_var_value = None
		
		itr_index_var = eval_args[0].to_text()
		if itr_index_var in engine.memory:
			old_var_value = engine.memory[itr_index_var]

		itr_index = 0
		while len(engine.alg_cache) >= repeat_level:
			if not isinstance(itr_index_var, type(None)):
				engine.memory[itr_index_var] = Number(itr_index_var, itr_index)
			
			engine.run(code)
			itr_index += 1
		
		if not isinstance(old_var_value, type(None)):
			engine.memory[itr_index_var] = old_var_value

		return None

