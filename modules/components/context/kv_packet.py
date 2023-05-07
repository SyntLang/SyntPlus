from typing import Self
from modules.components.context.memory import MemoryObject
from modules.components.context.void import Void

class KVPacket(MemoryObject):
	name: MemoryObject = Void()
	__value__: MemoryObject = Void()
	value: MemoryObject = None

	def __init__(self: Self,
			name: MemoryObject = None,
			value: MemoryObject = None
		) -> None:
		"""
		Collection type memory object
		"""

		if name: self.name = name
		if value: self.__value__ = value
		super().__init__(self.name, KVPacket, self.__value__)

		return None
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		return self.__value__.to_number()
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		return self.__value__.to_decimal()
	
	def to_text(self: Self) -> str:
		"""
		Convert object value to Text
		"""

		return self.__value__.to_text()
	
	def to_binary(self: Self) -> bool:
		"""
		Convert object value to Text
		"""

		return self.__value__.to_binary()

