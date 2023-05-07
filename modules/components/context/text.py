from typing import Self
from modules.components.context.memory import MemoryObject

class Text(MemoryObject):
	value: str = ""

	def __init__(self: Self,
			name: str|None = None,
			value: str = ""
		) -> None:
		"""
		Text(String) type memory object
		"""

		super().__init__(name, Text, value)

		return None
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		if not all([ch in "-0123456789.," for ch in str(self.value)]) or not self.value:
			return len(self.value)
		
		if str(self.value).count("-") > 1: return len(self.value)
		
		if not (str(self.value).startswith("-") if "-" in self.value else True):
			return len(self.value)
		
		if self.value.count(".") > 1: return len(self.value)
		return int(float(str(self.value).replace(",", "")))
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		if not all([ch in "0123456789.," for ch in str(self.value)]) or not self.value:
			return float(len(self.value))
		
		if str(self.value).count("-") > 1: return float(len(self.value))
		
		if not (str(self.value).startswith("-") if "-" in self.value else True):
			return float(len(self.value))
		
		if self.value.count(".") > 1: return float(len(self.value))
		return float(str(self.value).replace(",", ""))

