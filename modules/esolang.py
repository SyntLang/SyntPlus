from typing import Self
from modules.logger import Logger
from modules.iterator import Iterator
from modules.runtime import Runtime
from modules.components.functions import Modules
import modules.errors as errors
import os
import sys
import time

class Esolang:
	META: dict = {
		"NAME": "ESOLANG",
		"VERSION": "0.0.0",
		"VER_CODE": {
			"Release Version": 0,
			"Update Version": 0,
			"Iteration": 0
		}
	}

	DEBUG: bool = False

	ARGS: list = []
	CWD: str = ""

	MODE_I: int = 0
	MODE_F: int = 1
	MODE: int = MODE_I

	SOURCE_PATH: str|None = None
	SOURCE_CODE: str|None = None

	FORCED_EXIT_OPTION_NO_ERROR: int = 0
	FORCED_EXIT_OPTION_ERROR: int = 1
	FORCED_EXIT_OPTION: int = FORCED_EXIT_OPTION_ERROR

	exec_start_time: int = 0
	exec_halt_times: dict = {}

	logger: Logger = None
	iterator: Iterator = None
	runtime: Runtime = None

	def __init__(self: Self, meta: dict = {},
		logger: Logger = None, iterator: Iterator = None,
		runtime: Runtime = None, modules: Modules = None,
		debug: bool = False, forced_exit_option: int = None) -> None:
		"""
		Create an Esolang class for programming langauge
		"""

		self.META.update(meta)
		self.logger = Logger(exit_on_error=True)

		if not logger: self.logger.error("Logger missing", errors.ENGINE_ERROR)
		if not iterator: self.logger.error("Iterator missing", errors.ENGINE_ERROR)
		if not runtime: self.logger.error("Runtime missing", errors.ENGINE_ERROR)
		if not modules: self.logger.warning("Modules missing")

		if not isinstance(forced_exit_option, type(None)):
			self.FORCED_EXIT_OPTION = forced_exit_option
		if debug: self.DEBUG = True

		self.logger = logger
		self.iterator = iterator
		self.runtime = runtime
		self.runtime.version = self.META["VER_CODE"]
		if modules: self.runtime.push_to_memory(modules.algorithms)
		
		self.ARGS = sys.argv[1:] if len(sys.argv) > 1 else []
		self.CWD = os.getcwd()

		self.update_mode()

		return None
	
	def main(self: Self) -> None:
		"""
		Esolang Mainloop
		"""

		try:
			self.exec_start_time = time.time()
			self.start()
		except KeyboardInterrupt:
			self.handle_keyboard_interrupt()
		except Exception as exception:
			self.handle_engine_errors(exception)
		else:
			end_time = time.time()
			ignore_time = 0

			for halt in self.exec_halt_times:
				if halt > self.exec_halt_times[halt]: continue
				ignore_time += self.exec_halt_times[halt] - halt
			
			final_time = end_time - ignore_time - self.exec_start_time
			if self.DEBUG: self.logger.debug(f"Execution Time: {final_time:.6f}s")

			return None
		
		end_time = time.time()
		if self.DEBUG:
			self.logger.debug(f"Execution Time: {end_time - self.exec_start_time:.6f}s")

		return None
	
	def handle_engine_errors(self: Self, exception: Exception) -> None:
		"""
		Handle errors that occur in engine
		"""

		tb = exception.__traceback__
		while tb.tb_next is not None: tb = tb.tb_next

		err_file = tb.tb_frame.f_code.co_filename.split("\\")[-1]
		err_msg = f"{exception} ({tb.tb_lineno} {err_file})"
		self.logger.error(err_msg, errors.ENGINE_ERROR)
		
		return None
	
	def handle_keyboard_interrupt(self: Self) -> None:
		"""
		Handle keyboard interrupt errors
		"""

		if self.MODE == self.MODE_I: print(); self.logger.out("Exited."); sys.exit()

		print()
		if self.FORCED_EXIT_OPTION == self.FORCED_EXIT_OPTION_NO_ERROR: sys.exit()

		self.logger.error("Keyboard Interrupt Forced Exit", errors.FORCE_QUIT_ERROR)
		sys.exit()
	
	def update_mode(self: Self) -> None:
		"""
		Updates the mode of the engine
		"""

		if not self.ARGS: self.MODE = self.MODE_I; return None
		if "*i" in self.ARGS: self.MODE = self.MODE_I; return None
		if "*interactive" in self.ARGS: self.MODE = self.MODE_I; return None

		if "*f" in self.ARGS: self.MODE = self.MODE_F; return None
		if "*file" in self.ARGS: self.MODE = self.MODE_F; return None
		if any(str(arg).endswith(".synt") for arg in self.ARGS): self.MODE = self.MODE_F; return None

		return None
	
	def start(self: Self) -> None:
		"""
		Run the engine with appropriate mode.
		"""

		if self.MODE == self.MODE_I: self.interactive_mode(); return None
		if self.MODE == self.MODE_F: self.file_mode(); return None
		
		return None
	
	def interactive_mode(self: Self) -> None:
		"""
		Starts interactive mode
		"""

		running = True
		code = ""
		while running:
			if code in ["end", "exit"]: sys.exit()
			try:
				if not code: code = input(">>>"); continue
			except EOFError:
				continue

			code_line = input("...")
			if code_line: code += f"\n{code_line}"; continue

			iterated_code = self.iterator.iterate(code)
			code = ""

			self.runtime.run(iterated_code)

		return None
	
	def get_code_file_path(self: Self) -> str|None:
		"""
		Gets the path of code file
		"""

		if self.MODE != self.MODE_F: return None
		eligible_files = [arg for arg in self.ARGS if str(arg).endswith(".synt")]
		
		if not eligible_files: return None
		paths = [code_file for code_file in eligible_files]
		valid_files = [source_file for source_file in paths if os.path.isfile(source_file)]

		if not valid_files: return None
		return valid_files[0]
	
	def get_code_file_data(self: Self) -> str|None:
		"""
		Gets source code
		"""

		if not self.SOURCE_PATH: return None
		if not os.path.isfile(self.SOURCE_PATH): return None
		source_code = ""
		with open(self.SOURCE_PATH, "r") as source_file:
			source_code = source_file.read()

		return source_code
	
	def file_mode(self: Self) -> None:
		"""
		Code is selected from a file to run
		"""

		self.SOURCE_PATH = self.get_code_file_path()
		if not self.SOURCE_PATH:
			self.logger.error("No source file found", errors.SRC_ERROR)
			return None
		
		self.SOURCE_CODE = self.get_code_file_data()
		if not self.SOURCE_CODE:
			self.logger.warning("Source file is empty")
			return None
		
		iterated_code = self.iterator.iterate(self.SOURCE_CODE)
		self.runtime.run(iterated_code)

		return None

