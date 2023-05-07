from typing import Self

class MemoryObject:
	name: str|None = None
	type: any = None
	value: any = None
	help_data: str = "A Memory Object"

	def __init__(self: Self,
			name: str|None = None,
			type: any = None,
			value: any = None
		) -> None:
		"""
		Memory Object - could be function, variables or anything
		"""

		self.name = name
		self.type = type
		self.value = value

		return None
	
	def to_text(self: Self) -> str:
		"""
		Convert object value to Text
		"""

		if isinstance(self.value, type(None)): return ""
		return str(self.value)
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		if isinstance(self.value, type(None)): return 0
		return int(self.value)
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		if isinstance(self.value, type(None)): return 0.0
		return float(self.value)
	
	def to_binary(self: Self) -> bool:
		"""
		Convert object value to Binary(Boolean)
		"""

		return bool(self.to_decimal())

