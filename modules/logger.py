from typing import Self
import modules.errors as errors
import datetime
import sys
import os

class Logger:
	history = []

	PRODUCTION: int = 1
	ERROR: int = 2
	WARNING: int = 3
	DEBUG: int = 4
	level: int = WARNING

	EXIT_ON_ERROR: bool = False

	def __init__(self: Self, level: int = None, exit_on_error: bool = False) -> None:
		"""
		Initiate logger
		"""

		if level: self.level = level
		self.EXIT_ON_ERROR = exit_on_error

		return None
	
	@staticmethod
	def log_time() -> str:
		"""
		Gets current date and time in logging format
		"""

		time_data = f"{datetime.datetime.now():%d-%m-%Y %I:%M:%S %p %f micro-s}"
		return time_data
	
	def save_to_history(self: Self, data: str = None) -> None:
		"""
		Saves data to log history
		"""

		if not data: return None
		if "\x1b" not in data: self.history.append(data); return None

		plain_data = ["m".join(s.split("m")[1:]) for s in data.split("\x1b")[1:]]
		plain_data = [data.split("\x1b")[0]] + plain_data
		plain_data = "".join(plain_data)

		self.history.append(plain_data)

		return None

	def out(self: Self, msg: str = "", *args, break_line: bool = True) -> None:
		"""
		Prints given message normally
		"""

		_msg = "".join([str(msg)] + list(args))
		self.save_to_history(f"[{self.log_time()}]: {_msg}")
		if self.level >= self.PRODUCTION: print(_msg, end= "\n" * break_line)
		return None
	
	def error(self: Self, msg: str = None, error_type: errors.Error = None, *_) -> None:
		"""
		Error messages
		"""

		if not msg: return None
		if not error_type: self.error("Error Type Invalid", errors.LOGGER_ERROR); return None

		logged_error_msg = f"[{self.log_time()}]: [ERROR]: {error_type.data}: {msg}"
		self.save_to_history(logged_error_msg)

		error_msg = f"[\033[38;2;255;0;0;6;1mERROR\033[0m]: {error_type.data}: {msg}"
		if self.level >= self.ERROR: print(error_msg)
		if self.EXIT_ON_ERROR: sys.exit()
		
		return None
	
	def warning(self: Self, msg: str = None) -> None:
		"""
		Warning messages
		"""

		if not msg: return None

		logged_warn_msg = f"[{self.log_time()}]: [WARNING]: {msg}"
		self.save_to_history(logged_warn_msg)

		warn_msg = f"[\033[38;2;227;179;65;6;1mWARNING\033[0m]: {msg}"
		if self.level >= self.WARNING: print(warn_msg)
		
		return None
	
	def debug(self: Self, msg: str = None, *msgs) -> None:
		"""
		Debug messages
		"""

		if isinstance(msg, type(None)): return None
		
		_msg = msg
		if isinstance(msg, (list, tuple)): _msg = "".join([str(m) for m in msg])
		if msgs: _msg += "".join([str(m) for m in msgs])

		logged_debug_msg = f"[{self.log_time()}]: [DEBUG]: {_msg}"
		self.save_to_history(logged_debug_msg)

		debug_msg = f"[\033[38;2;65;195;227;6;1mDEBUG\033[0m]: {_msg}"
		if self.level >= self.DEBUG: print(debug_msg)
		
		return None
	
	def save_history(self: Self, path: str = None, *, new: bool = True) -> None:
		"""
		Saves console(logged only) history
		"""

		if not path: self.error("Path is required to save log history", errors.DIR_ERROR)
		save_content = "\n".join(self.history)

		if not self.history: return None
		
		mode = "a"
		if new or not os.path.isfile(path): mode = "w"

		log_dir = "/".join(path.replace("\\", "/").split("/")[:-1])
		if not os.path.isdir(log_dir): os.makedirs(log_dir)

		with open(path, mode) as log_file:
			log_file.write(save_content if mode == "w" else "\n" + save_content)

		return None

