from typing import Self
from modules.logger import Logger
from modules.components.context import (
	Module,
	Number,
	Text,
	Binary,
	Collection,
	Void,
	MemoryObject
)
import modules.errors as errors

class Operations(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Operations Module
		"""

		super().__init__("Operations", logger)
		self.module_functions = [
			(self.concatenate, "concatenate", "concat", ".."),
			(self.length, "length", "len", "#"),
			(self.reverse, "reverse"),
			(self.invert, "invert", "not"),
			(self.item, "item", "[]", "@")
		]

		return None
	
	def concatenate(self: Self, *args) -> Text:
		"""
		Adds two or more objects
		"""

		value = Text(None, "")
		for arg in args:
			value.value += arg.to_text()

		return value
	
	def length(self: Self, *args) -> Number:
		"""
		Returns length of an object.
		"""

		if not args: return Number(None, 0)
		if len(args) > 1:
			self.logger.error("Length can be used for one value only", errors.ARG_OVERFLOW_ERROR)
			return Void()
		
		return Number(None, len(args[0].to_text()))
	
	def invert(self: Self, *args) -> Binary|Void:
		"""
		Returns the inverted binary value of an object.
		"""

		if not args: return Binary(None, True)
		if len(args) > 1:
			self.logger.error("Only one value can be inverted", errors.ARG_OVERFLOW_ERROR)
			return Void()

		return Binary(None, not args[0].to_binary())
	
	def reverse(self: Self, *args) -> Text|Void:
		"""
		Returns the reversed text value of an object.
		"""

		if not args: return Text(None, "")
		if len(args) > 1:
			self.logger.error("Only one value can be reversed", errors.ARG_OVERFLOW_ERROR)
			return Void()

		if args[0].type == Collection:
			return Collection(None, args[0].value[::-1], args[0].index[::-1], args[0].connector)
		
		return Text(None, args[0].to_text()[::-1])
	
	def item(self: Self, *args) -> MemoryObject|Void:
		"""
		Gets an item in a collection or text value from its key.
		"""

		if len(args) < 1:
			self.logger.error("Object required to get item", errors.ARG_MISSING_ERROR)
			return Void()
		
		if len(args) < 2:
			self.logger.error("Index required to get item", errors.ARG_MISSING_ERROR)
			return Void()
		
		if len(args) > 2:
			self.logger.error("Only one index can be passed", errors.ARG_OVERFLOW_ERROR)
			return Void()
		
		iterable: Collection = args[0]
		index = args[1]

		if index.type == Collection:
			self.logger.error("Index can not be a collection", errors.ARG_TYPE_ERROR)
			return Void()
		
		if iterable.type != Collection:
			iterable = Collection(
				name = "--<" + iterable.name + ">-collection--" if iterable.name else None,
				value = [Text(None, ch) for ch in iterable.to_text()],
				index = [Number(None, i) for i in range(len(iterable.to_text()))]
			)

		item: MemoryObject|None = iterable.get(index)
		if isinstance(item, type(None)):
			self.logger.error("Invalid index", errors.KEY_ERROR)
			return Void()
		
		return item

