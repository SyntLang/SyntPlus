from typing import Self
from modules.logger import Logger
import modules.errors as errors

class Iterator:
	TERMINAL_CHARS: list = ["\n"]
	INDENT_CHARS: list = ["\t", "    "]

	original_code: str = None
	logger: Logger = None

	def __init__(self: Self, logger: Logger = None, **rules) -> None:
		"""
		Initiates iterator
		"""

		self.logger = Logger(exit_on_error=False)
		if not logger: self.logger.error("Logger missing", errors.ENGINE_ERROR)
		self.logger = logger

		self.update_rules(**rules)
		return None
	
	def update_rules(self: Self, **rules) -> None:
		"""
		Updates iterator rules
		"""

		for rule in rules:
			setattr(self, rule.upper(), rules[rule])
		
		return None
	
	def iterate(self: Self, code: str = None) -> list:
		"""
		Iterates over code
		"""

		if isinstance(code, type(None)):
			self.logger.error("No code", errors.SRC_ERROR)
			return []
		
		self.original_code = code
		if not self.original_code:
			self.logger.warning("No code")
			return []
		
		chunks = self.create_chunks(code)
		chunks = self.refactor_chunks(chunks)

		return chunks
	
	def create_chunks(self: Self, code: str = None, skip_to_line_id: int = 0) -> list:
		"""
		Creates chunks
		"""

		if not code: return []

		partial_code = self.convert_terminal_chars(code)
		terminal_lines = partial_code.split(self.TERMINAL_CHARS[0])
		
		chunks = []
		chunk = [None, []]

		for line_id, raw_line in enumerate(terminal_lines):
			if not raw_line.strip(): continue
			line = self.convert_indent_chars(raw_line)
			if line.startswith(self.INDENT_CHARS[0]):
				line = line.replace(self.INDENT_CHARS[0], "", 1)
				if chunk[0]: chunk[1].append(line); continue

				error_line_id = skip_to_line_id + line_id + 1
				error_msg = f"Unexpected Indentation in Line {error_line_id}:\n{raw_line}"
				self.logger.error(error_msg, errors.INDENT_ERROR)
				continue

			if any([ln.startswith(self.INDENT_CHARS[0]) for ln in chunk[1]]):
				arg_start_line = line_id - len(chunk[1])
				chunk_arg = self.TERMINAL_CHARS[0].join(chunk[1])
				chunk[1] = self.create_chunks(chunk_arg, arg_start_line)
			
			if chunk[0]: chunks.append(chunk)
			chunk = [line, []]
		else:
			if any([ln.startswith(self.INDENT_CHARS[0]) for ln in chunk[1]]):
				arg_start_line = skip_to_line_id + len(terminal_lines) - len(chunk[1])
				chunk_arg = self.TERMINAL_CHARS[0].join(chunk[1])
				chunk[1] = self.create_chunks(chunk_arg, arg_start_line)

			if chunk[0]: chunks.append(chunk)

		return chunks
	
	def refactor_chunks(self: Self, chunks: list = []) -> list:
		"""
		Refactor chunks to organize for easier runtime handling
		"""

		if not chunks: return []

		updated_chunks = []
		for chunk in chunks:
			if type(chunk) != list: updated_chunks.append(chunk); continue
			if not chunk[1]: updated_chunks.append(chunk[0]); continue
			
			if not any([(type(arg) == list) for arg in chunk[1]]):
				updated_chunks.append(chunk)
				continue

			arg_chunk = self.refactor_chunks(chunk[1])
			updated_chunks.append([chunk[0], arg_chunk])

		return updated_chunks
	
	def convert_terminal_chars(self: Self, code: str = None) -> str:
		"""
		Converts all terminal characters to first terminal character
		"""

		if not code: return ""

		partial_code = code
		for terminal_char in self.TERMINAL_CHARS:
			partial_code = partial_code.replace(terminal_char, self.TERMINAL_CHARS[0])
		
		return partial_code
	
	def convert_indent_chars(self: Self, code: str = None) -> str:
		"""
		Converts all terminal characters to first terminal character
		"""

		if not code: return ""

		partial_code = code
		for indent_char in self.INDENT_CHARS:
			partial_code = partial_code.replace(indent_char, self.INDENT_CHARS[0])
		
		return partial_code
	
	def encode(self: Self, instructions: list = [], *,
	    	indent_char: str = INDENT_CHARS[0],
		    terminal_char: str = TERMINAL_CHARS[0]
	    ) -> str:
		"""
		Converts a list of instructions into code
		"""

		if not instructions: return None
		encoded_data = ""
		
		for instruction in instructions:
			if type(instruction) == str:
				encoded_data += f"{terminal_char}{instruction}"
				continue
			
			encoded_data += f"{terminal_char}{instruction[0]}"
			if any(type(arg) == list for arg in instruction[1]):
				encoded_args_data_raw = self.encode(
					instruction[1],
					indent_char = indent_char,
					terminal_char = terminal_char
				)

				encoded_args_data = ""
				for arg_line in encoded_args_data_raw.split(terminal_char):
					encoded_args_data += f"{terminal_char}{indent_char}{arg_line}"
				
				encoded_args_data = encoded_args_data.replace(terminal_char, "", 1)
				
				encoded_data += f"{terminal_char}{encoded_args_data}"
				continue

			encoded_args_data = ""
			for arg_line in instruction[1]:
				encoded_args_data += f"{terminal_char}{indent_char}{arg_line}"
			
			encoded_args_data = encoded_args_data.replace(terminal_char, "", 1)
			
			encoded_data += f"{terminal_char}{encoded_args_data}"
		
		encoded_data = encoded_data.replace(terminal_char, "", 1)

		return encoded_data

