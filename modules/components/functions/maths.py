from typing import Self
from modules.logger import Logger
from modules.components.context import (
	Module,
	Decimal,
	Void
)
import modules.errors as errors

class Maths(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Maths Module
		"""

		super().__init__("Maths", logger)
		self.module_functions = [
			(self.add, "add", "+"),
			(self.subtract, "subtract", "-"),
			(self.multiply, "multiply", "mult", "*"),
			(self.quotient, "divide", "quotient", "/"),
			(self.remainder, "remainder", "modulo", "%"),
			(self.power, "power", "**", "^"),
			(self.negate, "negate", "~")
		]

		return None
	
	def add(self: Self, *args) -> Decimal:
		"""
		Adds two or more objects
		"""

		value = Decimal(None, 0)
		for arg in args:
			value.value += arg.to_decimal()

		return value
	
	def multiply(self: Self, *args) -> Decimal:
		"""
		Multiplies two or more objects
		"""

		value = Decimal(None, 1)
		for arg in args:
			value.value *= arg.to_decimal()

		return value
	
	def negate(self: Self, *args) -> Decimal|Void:
		"""
		Returns the negated decimal value of an object.
		"""

		if not args: return Decimal(None, 0.00)
		if len(args) > 1:
			self.logger.error("Only one value can be negated", errors.ARG_OVERFLOW_ERROR)
			return Void()

		return Decimal(None, - args[0].to_decimal())
	
	def subtract(self: Self, *args) -> Decimal|Void:
		"""
		Returns the value of object 1 - object 2.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require a subtrahend", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot have more than 1 subtrahend at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Decimal(None, args[0].to_decimal() - args[1].to_decimal())
	
	def quotient(self: Self, *args) -> Decimal|Void:
		"""
		Returns the quotient of object 1 / object 2.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require a divisor", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot have more than 1 divisors at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Decimal(None, args[0].to_decimal() / args[1].to_decimal())
	
	def remainder(self: Self, *args) -> Decimal|Void:
		"""
		Returns the remainder of object 1 / object 2.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require a divisor", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot have more than 1 divisors at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Decimal(None, args[0].to_decimal() % args[1].to_decimal())
	
	def power(self: Self, *args) -> Decimal|Void:
		"""
		Returns the value of object 1 raised to the power of object 2.
		"""

		if len(args) == 0:
			self.logger.error("Minimum two objects required", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) == 1:
			self.logger.error("Require an exponent", errors.ARG_MISSING_ERROR)
			return Void()
		elif len(args) > 2:
			self.logger.error(
				"Cannot have more than 1 exponents at a time",
		    	errors.ARG_OVERFLOW_ERROR
			)
			return Void()
		
		return Decimal(None, args[0].to_decimal() ** args[1].to_decimal())

