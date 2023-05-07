from typing import Self
from modules.components.context.memory import MemoryObject

class Decimal(MemoryObject):
	value: float = 0.0

	def __init__(self: Self,
			name: str|None = None,
			value: int = 0.0
		) -> None:
		"""
		Decimal(Float) type memory object
		"""

		super().__init__(name, Decimal, value)

		return None
	
	def to_binary(self: Self) -> bool:
		"""
		Converts to Binary
		"""
		
		return bool(self.value)

