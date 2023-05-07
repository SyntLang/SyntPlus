from typing import Self, Callable
from modules.components.context.memory import MemoryObject
from modules.components.context.void import Void
from modules.components.context.collection import Collection

class Algorithm(MemoryObject):
	code: Callable|str|None = None
	args_collection_name: str|None = None
	rich_data: bool = False
	help_data: str = ""

	def __init__(self: Self,
			name: str|None = None,
			code: Callable|str|None = None,
			help_data: str = "",
			rich_data: bool = False,
			need_engine: bool = False,
			*,
			args_collection_name: str|None = None
		) -> None:
		"""
		Algorithm type memory object
		"""

		super().__init__(name, Algorithm, code)
		self.code = code
		self.help_data = help_data.strip()
		self.rich_data = rich_data
		self.need_engine = need_engine
		self.args_collection_name = args_collection_name

		return None
	
	def run(self: Self, args: list[MemoryObject] = [], *,
			engine = None
		) -> None|MemoryObject:
		"""
		Run algorithm
		"""

		calculated_args = []
		for arg in args:
			if not isinstance(arg, list): calculated_args.append(arg); continue
			data = engine.run_chunk(arg)
			calculated_args.append(data)
			
		if not self.code: return None
		if callable(self.code):
			if not self.rich_data:
				return_value = self.code(*[arg.value for arg in calculated_args])
				return MemoryObject(value = return_value)
			
			if self.need_engine:
				return_value = self.code(*calculated_args, engine)
			else:
				return_value = self.code(*calculated_args)
			
			if isinstance(return_value, type(None)): return Void()
			return return_value
		
		iterated_code = engine.iterator.iterate(self.code)
		old_variable = None
		if self.args_collection_name:
			if self.args_collection_name in engine.memory:
				old_variable = engine.memory[self.args_collection_name]
			
			engine.memory[self.args_collection_name] = Collection(
				name = f"--args--{self.name}",
				value = args
			)
		
		engine.return_cache = Void()
		engine.run(iterated_code)
		return_data = engine.return_cache
		engine.__delattr__("return_cache")

		if self.args_collection_name:
			del engine.memory[self.args_collection_name]
			if old_variable:
				engine.memory[self.args_collection_name] = old_variable

		return return_data
	
	def to_text(self: Self) -> str:
		return self.name if self.name else ""

