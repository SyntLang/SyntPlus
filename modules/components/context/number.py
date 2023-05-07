from typing import Self
from modules.components.context.memory import MemoryObject

class Number(MemoryObject):
	value: int = 0

	def __init__(self: Self,
			name: str|None = None,
			value: int = 0
		) -> None:
		"""
		Number(Integer) type memory object
		"""

		super().__init__(name, Number, int(value))

		return None
	
	def to_binary(self: Self) -> bool:
		"""
		Converts to Binary
		"""
		
		return bool(self.value)

