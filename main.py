import sys
if sys.version_info < (3, 11): sys.exit(f"Python {sys.version} unsupported")

from modules import (
	Esolang,
	logger,
	iterator,
	runtime,
	engine_modules
)

synt = Esolang(
	{
		"NAME": "Synt",
		"VERSION": "1.0.0",
		"VER_CODE": {
			"Model": "Plus",
			"Release Version": 1,
			"Update Version": 0,
			"Iteration": 0
		}
	},
	logger = logger,
	iterator = iterator,
	runtime = runtime,
	modules = engine_modules,
	debug = False
)

if __name__ == "__main__":
	synt.main()

