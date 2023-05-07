from typing import Self
from modules.components.context.memory import MemoryObject
from modules.components.context.text import Text
from modules.components.context.number import Number

class Collection(MemoryObject):
	value: list = []
	index: list = []
	connector: Text = Text(None, "")

	def __init__(self: Self,
			name: str|None = None,
			value: list[MemoryObject] = [],
			index: list[MemoryObject] = [],
			connector: Text = Text(None, "")
		) -> None:
		"""
		Collection type memory object
		"""

		super().__init__(name, Collection, value)
		self.index = index
		self.connector = connector
		if type(connector) == str:
			self.connector = Text(f"--{name}-connector--", connector)
		
		if len(index) < len(value):
			itr_index = 0
			for _ in range(len(value) - len(index)):
				while itr_index in [i.value for i in self.index]:
					itr_index += 1
				
				self.index.append(Number(None, itr_index))
				itr_index += 1

		return None
	
	def to_number(self: Self) -> int:
		"""
		Convert object value to Number
		"""

		return int(len(self.value))
	
	def to_decimal(self: Self) -> float:
		"""
		Convert object value to Decimal
		"""

		return float(len(self.value))
	
	def to_binary(self: Self) -> float:
		"""
		Convert object value to Binary
		"""

		return bool(len(self.value))
	
	def to_text(self: Self) -> str:
		"""
		Convert object value to Text
		"""

		return self.connector.to_text().join([v.to_text() for v in self.value if v])
	
	def get(self: Self, key: MemoryObject) -> MemoryObject|None:
		"""
		Get object from its key in collection
		"""

		for index, value in zip(self.index, self.value):
			if index.value == key.value: return value

		return None

