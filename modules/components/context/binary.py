from typing import Self
from modules.components.context.memory import MemoryObject

class Binary(MemoryObject):
	value: bool = False

	def __init__(self: Self,
			name: str|None = None,
			value: bool = False
		) -> None:
		"""
		Binary(Boolean) type memory object
		"""

		super().__init__(name, Binary, bool(value))

		return None
	
	def to_text(self: Self) -> str:
		"""
		Convert object value to string
		"""

		return "TRUE" if self.value else "FALSE"
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		return 1 if self.value else 0
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		return 1.0 if self.value else 0.0

