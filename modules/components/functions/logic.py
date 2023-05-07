from typing import Self
from modules.logger import Logger
from modules.components.context import Module, Binary, Void
import modules.errors as errors

class Logic(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Logic Module
		"""

		super().__init__("Logic", logger)
		self.structure_functions = [
			(self.condition, "if")
		]
		self.module_functions = [
			(self.logic_and, "all", "and", "&&"),
			(self.logic_or, "any", "or", "||"),
			(self.logic_equal, "equal", "=="),
			(self.logic_unequal, "unequal", "!="),
			(self.logic_lesser, "lesser", "<"),
			(self.logic_greater, "greater", ">"),
			(self.logic_lesser_equal, "notgreater", "lesser-or-equal", "<=", "!>"),
			(self.logic_greater_equal, "notlesser", "greater-or-equal", ">=", "!<")
		]

		return None

	def condition(self: Self, engine, code: list, run_data: list) -> None:
		"""
		Conditional Process
		"""

		args = run_data[1:]
		eval_args = []
		
		if not len(args):
			self.logger.error("Conditional Binary Required", errors.ARG_MISSING_ERROR)
			return None
		
		args = args[0].replace(", ", ",")
		args = args.split(",")
		eval_args = engine.evaluate_args(args)
		
		condition_state = False
		if len(eval_args):
			condition_state = all(arg.to_binary() for arg in eval_args)
		
		if condition_state:
			engine.run(code)

		return None
	
	def logic_and(self: Self, *args) -> Binary:
		"""
		Returns the collective binary value of one object or more.
		"""

		if not args: return Binary(None, False)

		return Binary(None, all([arg.to_binary() for arg in args]))
	
	def logic_or(self: Self, *args) -> Binary:
		"""
		Returns if any object has true binary value.
		"""

		if not args: return Binary(None, False)

		return Binary(None, any([arg.to_binary() for arg in args]))
	
	def logic_equal(self: Self, *args) -> Binary|Void:
		"""
		Returns true if all objects are equal, else false.
		"""

		if len(args) < 2:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		
		are_equal = True
		compare_from_string = False
		compare_value = args[0].to_decimal()

		for arg in args:
			if arg.to_text() not in [str(arg.to_number()), str(arg.to_decimal())]:
				compare_from_string = True
				compare_value = arg.to_text()
				break
		
		for arg in args:
			if compare_from_string:
				if compare_value != arg.to_text(): are_equal = False; break
			else:
				if compare_value != arg.to_decimal(): are_equal = False; break
		
		return Binary(None, are_equal)
	
	def logic_unequal(self: Self, *args) -> Binary|Void:
		"""
		Returns false if all objects are equal, else true.
		"""

		logic_equal_data = self.logic_equal(*args)
		if logic_equal_data.type == Void: return Void()

		are_unequal = not logic_equal_data.to_binary()

		return Binary(None, are_unequal)
	
	def logic_greater(self: Self, *args) -> Binary|Void:
		"""
		Returns true if all object 1 > object 2, else false.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require an object to compare from", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot compare from more than 1 objects at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Binary(None, args[0].to_decimal() > args[1].to_decimal())
	
	def logic_lesser(self: Self, *args) -> Binary|Void:
		"""
		Returns true if all object 1 < object 2, else false.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require an object to compare from", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot compare from more than 1 objects at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Binary(None, args[0].to_decimal() < args[1].to_decimal())
	
	def logic_greater_equal(self: Self, *args) -> Binary|Void:
		"""
		Returns true if all object 1 > object 2 or equal, else false.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require an object to compare from", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot compare from more than 1 objects at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Binary(None, args[0].to_decimal() >= args[1].to_decimal())
	
	def logic_lesser_equal(self: Self, *args) -> Binary|Void:
		"""
		Returns true if all object 1 < object 2 or equal, else false.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require an object to compare from", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot compare from more than 1 objects at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Binary(None, args[0].to_decimal() <= args[1].to_decimal())

