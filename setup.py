from cx_Freeze import setup, Executable

base = None

executables = [Executable("color.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':['colorama', 'termcolor'],
    },
}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
