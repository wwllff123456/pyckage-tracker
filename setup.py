from cx_Freeze import setup, Executable


setup(
	name = "Pyckage Tracker",
	version = "0.3",
	author="Lifu",
	description="Package tracker in python",
	executables = [Executable("main.py", icon = "icon.ico")]
	)

