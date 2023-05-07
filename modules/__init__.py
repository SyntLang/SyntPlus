from modules.esolang import Esolang
from modules.logger import Logger
from modules.iterator import Iterator
from modules.runtime import Runtime
from modules.components.functions import (
    Modules,
    Comments,
    IO,
    Variable,
    System,
    Operations,
    Maths,
    Loops,
    Logic
)

logger = Logger(
	level = Logger.DEBUG,
	exit_on_error = False
)
iterator = Iterator(
	logger = logger
)
runtime = Runtime(
	logger = logger,
    iterator = iterator
)
engine_modules = Modules(
	modules = [
        Comments,
		IO,
        Variable,
        System,
        Operations,
        Maths,
        Loops,
        Logic,
	],
	logger = logger
)

