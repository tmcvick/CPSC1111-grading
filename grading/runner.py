import itertools
import locale
import os
from subprocess import Popen, PIPE
from threading import Timer


class Runner:
    """Class to run programs and capture output
    """
    __executable = None
    __stderr = None
    __stdout = None
    __error = ''
    __encoding = locale.getdefaultlocale()[1]

    def __init__(self, executable=None):
        if (os.path.isfile(executable) and os.access(executable, os.X_OK)) or 'make' in executable:
            self.__executable = executable
        else:
            print("Executable passed to constructor {0} does not exist!".format(executable))

    def run(self, args={}, input=[], timeout=None):
        """Run the specified executable
        'args' is a list of command line arguments to provide the executable
        'input' is a list of input strings to be passed to the proc's stdin
        'timeout' kill process after 'timeout' seconds if provided
        """
        args_list = list(itertools.chain(*(args.items())))     # Flatten dict to list
        args_list = list(filter(lambda x: x != '', args_list))       # Remove blanks

        # Generate command
        cmd = [self.__executable] + args_list
        print('Executing command: {0}\nInput: {1}\n'.format(cmd, input))
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        if timeout:
            # Timer function
            def timeout_kill(p):
                print("Timeout, killing child process...")
                p.kill()
                self.__error = 'Timeout'

            timer = Timer(timeout, timeout_kill, [proc])
            try:
                timer.start()
                output = proc.communicate('\n'.join(input).encode())
                self.__stdout = output[0].decode(self.__encoding)
                self.__stderr = output[1].decode(self.__encoding)
            finally:
                timer.cancel()
        else:
            output = proc.communicate('\n'.join(input).encode())
            self.__stdout = output[0].decode(self.__encoding)
            self.__stderr = output[1].decode(self.__encoding)
        return proc.returncode, args_list

    def make(self, target=None, input=[], output=PIPE, timeout=None, rootdir=None, username=None):
        """Execute the Make command
        'target' is the target of make we want to use
        'input' is a list of input strings to be passed to the proc's stdin
        'output' is where we want to direct the program's output, PIPE by default, pass in open File object
        'timeout' kill process after 'timeout' seconds if provided
        """
        # Generate command
        cmd = ['make', '-C', '{0}{1}/'.format(rootdir, username), '{0}'.format(target)]if target else ['make']
        print('Executing command: {0}\nInput: {1}\n'.format(cmd, input))
        proc = Popen(cmd, stdout=output, stderr=output, stdin=PIPE)

        if timeout:
            # Timer function
            def timeout_kill(p):
                print("Timeout, killing child process...")
                p.kill()
                self.__error = 'Timeout'

            timer = Timer(timeout, timeout_kill, [proc])
            try:
                timer.start()
                output = proc.communicate('\n'.join(input).encode())
                self.__stdout = output[0].decode(self.__encoding)
                self.__stderr = output[1].decode(self.__encoding)
            finally:
                timer.cancel()
        else:
            output = proc.communicate('\n'.join(input).encode())
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

    def error(self):
        """Return the error string set during the execution of the child process
        Empty string if no error
        """
        return self.__error
