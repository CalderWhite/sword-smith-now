"""Simply writes the arguments provided to the provided shell's stdout, in a nice fashion."""
from modules import commandLine
def run(*args):
    """Executes the command"""
    if len(args) < 1:
        raise TypeError("Missing argument 0 : commandLine.shell")
    elif len(args) < 2:
        raise TypeError("Missing argument 1: args[]")
    shell = args[0]
    args = args[1]
    if len(args) > 0:
        if type(args[0]) in [list,tuple]:
            message = ",".join(args[0])
        else:
            message = str(args[0])
        shell.stdout.writeLine(message)
    else:
        raise commandLine.missingArgumentError("message")