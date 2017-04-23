from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter
import os

INPUT = ['80', '90', '70', '100', '60', '90',
         '85', '78', '93', '80', '70', '98',
         '98', '85', '100', '99', '89', '90',
         '72', '0', '78', '98', '100', '65',
         '67', '11', '28', '89', '85', '90',
         '98', '85', '87', '56', '69', '22',
         '85', '72', '95', '75', '64', '88']


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.FILENAME = 'mainDriver.c'
        self.EXENAME = 'lab11'
        self.__compiler = None

        self.__scores = {
            'Functionality': {'value': 0, 'max': 85, 'comment': ''},
            'noWarnings': {'value': 5, 'max': 5, 'comment': ''},
            'Formatting': {'value': 0, 'max': 10, 'comment': ''}
        }


    def grade_lab11(self, output):
        return

    def grade(self, username, rootdir):
        output_lines = ''
        reporter = Reporter(username, rootdir)
        print("*********************")
        print("Grading {0}".format(username))
        print("*********************")

        # Compile program with flags
        if os.path.isfile('{0}{1}/Makefile'.format(rootdir, username)) or os.path.isfile(
                '{0}{1}/makefile'.format(rootdir, username)):
            print('=== Found Makefile! ===\n')

            # Run program with input and timeout
            runner = Runner('make')
            return_code = runner.make(timeout=3, target='run', rootdir=rootdir, username=username, input=INPUT)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                self.grade_lab11(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute: {0}'.format(
                    runner.error() + runner.stdout() + runner.stderr())
        else:
            print('!!! Did not find makefile !!!')
            self.__scores['Functionality']['comment'] = 'No makefile!'

        reporter.report_scores(self.__scores, username, INPUT, output_lines)
