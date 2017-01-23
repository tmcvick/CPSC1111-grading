import subprocess
import itertools
import locale

class Compiler:
    """Class that can be used to compile programs from source and capture output
    Supports:
        C (gcc, clang)
    """
    __source = []
    __stderr = None
    __stdout = None
    __encoding = locale.getdefaultlocale()[1]

    def __init__(self, source=[]):
        self.__source = source

    def gcc_compile(self, flags={}):
        """Compiles source files provided in constructor with GCC.
        Additional flags may be passed with the 'flags' hash
        Does not produce warnings by default
        Returns the exit code of the compiler
        """
        flag_list = list(itertools.chain(*(flags.items())))     # Flatten dict to list
        flag_list = list(filter(lambda x: x != '', flag_list))  # Remove blanks

        cmd = ['gcc'] + self.__source + flag_list
        print('Executing command: {0}\n'.format(cmd))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = proc.communicate()
        self.__stdout = output[0].decode(self.__encoding)
        self.__stderr = output[1].decode(self.__encoding)
        return proc.returncode

    def clang_compile(self, flags={}):
        """Compiles source files provided in constructor with Clang.
        Additional flags may be passed with the 'flags' hash
        Does not produce warnings by default
        Returns the exit code of the compiler
        """
        flag_list = list(itertools.chain(*(flags.items())))     # Flatten dict to list
        flag_list = filter(lambda x: x != '', flag_list)        # Remove blanks

        cmd = ['clang'] + self.__source + flag_list
        print('Executing command: {0}'.format(cmd))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = proc.communicate()
        self.__stdout = output[0].decode(self.__encoding)
        self.__stderr = output[1].decode(self.__encoding)
        return proc.returncode

    def stdout(self):
        """Return contents of stdout buffer produced from the last compilation.
        If no compilation has been run, returns None.
        """
        return self.__stdout

    def stderr(self):
        """Return contents of stderr buffer produced from the last compilation.
        If no compilation has been run, returns None.
        """
        return self.__stderr

    def clear(self):
        self.__stderr = None
        self.__stdout = None
        self.__source = []