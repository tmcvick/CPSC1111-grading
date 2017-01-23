import os

from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter


class Script:

    __compiler = None

    __scores = {
        'formatting': {'value': 0, 'max': 10, 'comment': ''},
        'functionality': {'value': 0, 'max': 90, 'comment': ''}
    }

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'formatting':       {'value': 0, 'max': 10, 'comment': ''},
            'functionality':    {'value': 0, 'max': 90, 'comment': ''}
        }

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/lab1.c'.format(rootdir, username)])
        compile_code = self.__compiler.gcc_compile({'-o': '{0}{1}/lab1'.format(rootdir, username), '-Wall': ''})
        if compile_code == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            # Run program with input and timeout
            runner = Runner('{0}{1}/lab1'.format(rootdir, username))
            return_code, args_list = runner.run(timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower().strip('!.') for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                output_lines = [line.replace(',','') for line in output_lines]                      # remove commas
                output_lines = list(filter(lambda x: x == 'hello world', output_lines))             # Filter for the correct text
                # Let's be a little leniant...
                if 10 <= len(output_lines):
                    print('Found {0} \"Hello World\" lines!'.format(len(output_lines)))
                    self.__scores['functionality']['value'] = 90
                else:
                    print('Output incorrect, found {0} correct lines (-90)'.format(len(output_lines)))
                    self.__scores['functionality']['value'] = 0
                    self.__scores['functionality']['comment'] = 'Incorrect number of \"Hello World!\"s (found {0})'.format(len(output_lines))
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['functionality']['value'] = 0
                self.__scores['functionality']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['functionality']['value'] = 0
            self.__scores['functionality']['comment'] = 'Failed to compile + {0}'.format(compile_code)

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username)
