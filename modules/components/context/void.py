from typing import Self
from modules.components.context.memory import MemoryObject

class Void(MemoryObject):
	def __init__(self: Self,
			name: str|None = None,
		) -> None:
		"""
		Algorithm type memory object
		"""

		super().__init__(name, Void, None)

		return None
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		return 0
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		return 0.0

