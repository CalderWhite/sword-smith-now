import pygame, importlib
# Error Classes
class missingArgumentError(Exception):
    """Error class used by commands if a required argument is not supplied."""
    def __init__(self,missing):
        message = "Missing \"%s\" argument." % missing
        super(missingArgumentError, self).__init__(message)
class commandNotFoundError(Exception):
    """Error class used by commmandLine file/class if a command was attempted to be executed and does not exist."""
    def __init__(self,command):
        message = "Command \"%s\" was not found." % command
        super(commandNotFoundError,self).__init__(message)
# Shell Classes
class outLine(object):
    """Contains basic functions, similar to io.StringIO."""
    def __init__(self,shell):
        self.shell = shell
    def write(self,message):
        """Appends text straight to the StandardOut."""
        self.shell.text+=message
    def writeLine(self,message):
        """Appends text to the StandardOut, with a line break on the end (\n)."""
        self.shell.text+=message + "\n"
class inLine(object):
    """Contains basic functions, similar to io.StringIO."""
    def __init__(self,shell):
        self.shell = shell
    def read(self):
        """Returns all the text in Standard Out. No filtering."""
        return self.shell.text
    def readLines(self):
        """Returns an array of all text in the Standard Out, split by line breaks (\n). If the last character is a line break, it will be filtered out."""
        split = self.shell.text.split("\n")
        if len(split) == 0:
            return []
        else:
            return split[:-1]
class shell(object):
    """Contains the basic string functions of a shell. Also command execution."""
    def __init__(self):
        self.text = ""
        self.stdout = outLine(self)
        self.stdin = inLine(self)
    def execute(self,command,*args):
        """Attempts to run the command (String parameter), and supplies the command with the args parameter"""
        # depending on where this is being executed, the import argument will differ
        if __name__ != '__main__':
            pre = "modules.commands."
        else:
            pre = "commands."
        try:
            # import the command
            commandMod = importlib.import_module(pre + command)
        except ImportError:
            raise commandNotFoundError(command)
        else:
            # execution of command
            if __name__ != '__main__':
                commandMod.run(self,args)
            else:
                commandMod.__getattribute__(command).run(self,args)
    def interperate(self,s):
        """Interperates the parameter "s" according to shell syntax.
Example:
    
    shell.interperate("/say hello")

Output:

    hello

Example:
    
    shell.interperate("Hello World.")

Output:
    
    Hello World.

        """
        # check if the string is a command
        args = []
        inString = False
        for i in s:
            if i == "\"" and inString == False:
                inString = True
            elif i == "\"" and inString:
                inString = False
            elif i == " " and not inString:
                args.append("")
            else:
                if len(args) == 0:
                    args.append(i)
                else:
                    args[-1]+=i
        if args[0][0] == "/":
            try:
                self.execute(args[0][1:],args[1::])
            except commandNotFoundError:
                self.execute("say",["command \"%s\" not found." % args[0][1:]])
        else:
            self.execute("say",s)
class cmd(object):
    def __init__(self,parent):
        self.inp = []
        self.parent = parent
        self.sh = shell()
    def execute_inline(self):
        """Executes whatever is inside self.inp (what the user has typed). This assumes there is something in self.inp"""
        # this assumes there is something in self.inp. If not it will attempt to execute nothing.
        s = "".join(self.inp)
        self.sh.interperate(s)
        # clear out the users input "cache"
        self.inp = []  
    def addChar(self,k):
        if len(k) > 0:
            if ord(k) == pygame.K_ESCAPE:
                self.parent.escape_current()
            elif ord(k) == pygame.K_BACKSPACE:
                if len(self.inp) > 0:
                    self.inp.pop(-1)
            elif ord(k) == pygame.K_RETURN:
                if len(self.inp):
                    self.execute_inline()
            else:
                self.inp.append(k)
    def capture(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.parent.quit()
            elif event.type == pygame.KEYDOWN:
                self.addChar(event.unicode)
if __name__ == '__main__':
    l = shell()
    l.interperate(input(">"))
    print(l.stdin.read())