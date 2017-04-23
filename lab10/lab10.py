from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter
import os


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.FILENAME = 'reverse_echo.c'
        self.EXENAME = 'lab10'
        self.__compiler = None

        self.__scores = {
            'Functionality': {'value': 0, 'max': 75, 'comment': ''},
            'makefile': {'value': 0, 'max': 15, 'comment': ''},
            'Formatting': {'value': 0, 'max': 10, 'comment': ''}
        }

    def grade_lab10(self, output):
        return

    def grade(self, username, rootdir):
        output_lines = ''
        reporter = Reporter(username, rootdir)
        print("*********************")
        print("Grading {0}".format(username))
        print("*********************")

        # Compile program with flags
        if os.path.isfile('{0}{1}/Makefile'.format(rootdir, username)) or os.path.isfile('{0}{1}/makefile'.format(rootdir, username)):
            print('=== Found Makefile! ===\n')
            self.__scores['makefile']['value'] = self.__scores['makefile']['max']

            # Run program with input and timeout
            runner = Runner('make')
            return_code = runner.make(timeout=3, target='test', rootdir=rootdir, username=username)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                self.grade_lab10(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute: {0}'.format(
                    runner.error() + runner.stdout() + runner.stderr())
        else:
            print('!!! Did not find makefile !!!')
            self.__scores['makefile']['comment'] = 'Did not find makefile'

        reporter.report_scores(self.__scores, username, 'make test', output_lines)
