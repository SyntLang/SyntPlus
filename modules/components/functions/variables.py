from typing import Self
from modules.logger import Logger
from modules.components.context import (
	MemoryObject,
	Module,
	Text,
	Number,
	Decimal,
	Binary,
	Void,
	Collection,
	KVPacket,
	Algorithm
)
import modules.errors as errors

class Variable(Module):
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None) -> None:
		"""
		Variable Module
		"""

		super().__init__("Variable", logger)
		self.module_functions = [
			(self.var, "var", "Var"),
			(self.text, "text", "Text", "string", "str"),
			(self.number, "number", "Number", "num", "int"),
			(self.decimal, "decimal", "Decimal", "float"),
			(self.binary, "binary", "Binary", "boolean", "bool", "bin"),
			(self.void, "void", "Void"),
			(self.collection, "collection", "Collection"),
			(self.kv_packet, "kv", "KV-Packet", "kvp")
		]
		self.engine_functions = [
			self.var
		]
		self.structure_functions = [
			(self.algorithm, "alg", "algorithm", "def", "define", "func", "function"),
			(self.result, "result", "return")
		]

		return None

	def var(self: Self, *args) -> None|Text|Number|Decimal|Binary|Void:
		"""
		Creates a variable
		"""

		engine = args[-1]
		if engine and len(engine.alg_cache[-1]) < 3:
			self.logger.error("Name required to create a variable", errors.RETURN_VAR_ERROR)
			return None
		
		if len(args) == 1:
			self.logger.error("Type required to create a variable", errors.ARG_MISSING_ERROR)
			return None
		
		var_name = engine.alg_cache[-1][2] if engine else None
		var_type = args[0].to_text()
		value = None

		if len(args) > 2:
			value = args[1]

		match var_type:
			case "TEXT"|"Text"|"text":
				if isinstance(value, type(None)): return Text(var_name)
				return Text(var_name, value.to_text())
			case "NUMBER"|"Number"|"number":
				if isinstance(value, type(None)): return Number(var_name)
				return Number(var_name, value.to_number())
			case "DECIMAL"|"Decimal"|"decimal":
				if isinstance(value, type(None)): return Decimal(var_name)
				return Decimal(var_name, value.to_decimal())
			case "BINARY"|"Binary"|"binary":
				if isinstance(value, type(None)): return Binary(var_name)
				return Binary(var_name, value.to_binary())
			case "VOID"|"Void"|"void"|"NONE"|"NOTHING"|"EMPTY":
				return Void(var_name)

		self.logger.error(f"Unknown Type: {var_type}", errors.ARG_TYPE_ERROR)
		return None
	
	def text(self: Self, *args) -> Text:
		"""
		Creates a variable of type Text
		"""

		return self.var(
			Text(None, "text"),
			Text(None, "".join(arg.to_text() for arg in args)),
			None
		)
	
	def number(self: Self, *args) -> Number:
		"""
		Creates a variable of type Number
		"""

		return self.var(
			Text(None, "number"),
			Number(None, sum([arg.to_number() for arg in args])),
			None
		)
	
	def decimal(self: Self, *args) -> Decimal:
		"""
		Creates a variable of type Decimal
		"""

		return self.var(
			Text(None, "decimal"),
			Decimal(None, sum([arg.to_decimal() for arg in args])),
			None
		)
	
	def binary(self: Self, *args) -> Binary:
		"""
		Creates a variable of type Binary
		"""

		return self.var(
			Text(None, "binary"),
			Binary(None, all([arg.to_binary() for arg in args]) and bool(args)),
			None
		)
	
	def void(self: Self, *args) -> Void:
		"""
		Creates a variable of type Void
		"""

		return self.var(
			Text(None, "void"),
			None
		)
	
	def collection(self: Self, *args) -> Collection:
		"""
		Creates a Collection
		"""

		id_args: list[MemoryObject] = []
		kw_args: list[KVPacket] = []

		for arg in args:
			if isinstance(arg, KVPacket): kw_args.append(arg); continue
			id_args.append(arg)
		
		indices = []
		values = []

		connector = ""
		for arg in kw_args:
			if arg.name.value == "connector":
				connector = arg.value
				continue

			values.append(arg)
			indices.append(arg.name)
		
		itr_index = 0
		for arg in id_args:
			values.append(arg)
			while itr_index in [i.value for i in indices]:
				itr_index += 1
			
			indices.append(Number(None, itr_index))
			itr_index += 1
		
		return Collection(
			None,
			value = values,
			index = indices,
			connector = connector
		)
	
	def kv_packet(self: Self, *args) -> KVPacket:
		"""
		Creates a Key Value Packet
		"""

		if len(args) < 2:
			if not len(args):
				self.logger.error("Name required for KV Packet.", errors.ARG_MISSING_ERROR)
				return None
			self.logger.error("Value required for KV Packet.", errors.ARG_MISSING_ERROR)
			return None

		return KVPacket(
			name = args[0],
			value = args[1]
		)
	
	def algorithm(self: Self, engine, code: list, run_data: list) -> None:
		"""
		Creates custom algorithms
		"""

		args = run_data[1:]
		eval_args = []
		
		if not len(args):
			self.logger.error("Algorithm name required", errors.ARG_MISSING_ERROR)
			return None
		
		args = args[0].replace(", ", ",")
		args = args.split(",")
		eval_args = engine.evaluate_args(args, no_var = True)
		
		alg_name = eval_args[0].to_text()
		encoded_instructions = engine.iterator.encode(code)
		args_collection_name = None

		if len(eval_args) > 1:
			args_collection_name = eval_args[1].to_text()

		engine.memory[alg_name] = Algorithm(
			name = alg_name,
			code = encoded_instructions,
			args_collection_name = args_collection_name
		)

		return None
	
	def result(self: Self, engine, code: list, run_data: list) -> None:
		"""
		Stops the current algorithm/structure process to continue
		"""

		args = engine.evaluate_args(code)
		algs_data = [[n, alg] for n, alg in enumerate(engine.alg_cache) if alg[0] == 1]

		if len(algs_data) < 1:
			self.logger.error("Cannot result out of an algorithm", errors.OUT_OF_BOUND_ERROR)
			return None
		
		if len(args) > 1:
			self.logger.error("You can result atmost one value only", errors.RETURN_VAR_ERROR)
			return None
		
		args += [Void()]
		
		for exit_itr in range(len(engine.alg_cache) - algs_data[-1][0] - 1):
			del engine.alg_cache[-1]
		
		engine.return_cache = args[0]
		return None

