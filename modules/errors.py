from typing import Self

class Error:
	CODE: str = "-1"
	NAME: str = "Random"
	CATEGORY: str = "Random"

	data: str = ""

	def __init__(self: Self, code: str = "-1", name: str = "Random",
		catergory: str = "Random") -> None:
		"""
		Initiates an error object
		"""

		self.CODE = code
		self.NAME = name
		self.CATEGORY = catergory

		self.data = self.format_error()

		return None

	def format_error(self: Self) -> str:
		"""
		Returns error in a formatted manner(with colors and typograhy)
		"""
		
		reset = "\033[0m"
		bold = "\033[1m"
		yellow_bold = "\033[38;2;227;179;65;1;3m"
		red_bold_italic = "\033[38;2;255;0;0;1;3m"

		code = self.CODE
		name = f"{self.NAME.upper()} ERROR"

		data = f"({yellow_bold}CODE: {red_bold_italic}{code}{reset}) {bold}{name}{reset}"
		
		return data

ENGINE_ERROR = Error("0a", "Engine", "Core")
LOGGER_ERROR = Error("0b", "Logger", "Core")
MODULE_ERROR = Error("0c", "Module", "Core")
FORCE_QUIT_ERROR = Error("4x", "Forced Exit", "Core")
NOT_IMPLEMENTED_ERROR = Error("10a", "Not Implemented", "Core")
DEPRECATED_ERROR = Error("10b", "Deprecated", "Core")

RANDOM_ERROR = Error("1x", "Random", "Random")

DIR_ERROR = Error("2a", "Directory", "Path")
FILE_ERROR = Error("2b", "File", "Path")

SRC_ERROR = Error("3x", "Source", "Code")
UNDEF_ANY_ERROR = Error("6a", "Undefined Object", "Code")
UNDEF_ALG_ERROR = Error("6b", "Undefined Algorithm", "Code")
KEY_ERROR = Error("9a", "Key", "Value")
VALUE_ERROR = Error("9b", "Value", "Value")

INDENT_ERROR = Error("5x", "Indentation", "Syntax")
RETURN_VAR_ERROR = Error("7x", "Return Variable", "Syntax")
ARG_MISSING_ERROR = Error("8a", "Argument Missing", "Syntax")
ARG_TYPE_ERROR = Error("8b", "Argument Type", "Syntax")
ARG_OVERFLOW_ERROR = Error("8c", "Argument Overflow", "Syntax")
OUT_OF_BOUND_ERROR = Error("11x", "Bound", "Syntax")

