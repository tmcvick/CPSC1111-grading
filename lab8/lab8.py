from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter

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
        self.FILENAME = 'lab8.c'
        self.EXENAME = 'lab8'
        self.__compiler = None

        self.__scores = {
            'Functionality': {'value': 0, 'max': 75, 'comment': ''},
            'noWarnings': {'value': 0, 'max': 5, 'comment': ''},
            'scanf': {'value': 0, 'max': 5, 'comment': ''},
            'array2d': {'value': 0, 'max': 5, 'comment': ''},
            'Formatting': {'value': 0, 'max': 10, 'comment': ''}
        }
#         self.SEARCH_FIRST = ['80', '90', '70', '100', '60', '90',
#                              '85', '78', '93', '80', '70', '98',
#                              '98', '85', '100', '99', '89', '90',
#                              '72', '0', '78', '98', '100', '65',
#                              '67', '11', '28', '89', '85', '90',
#                              '98', '85', '87', '56', '69', '22',
#                              '85', '72', '95', '75', '64', '88']
#         self.SEARCH_SECOND = ['81.67', '84.00', '93.50', '68.83', '61.67', '69.50', '79.83']
#         self.SEARCH_THIRD = ['83.57', '60.14', '78.71', '86.19', '76.71', '77.57']
#         self.SEARCH_FOURTH = """0 11 22 28 56 60 64 65 67 69 70 70 72 72 75 78 78 80 80 85 85 85 85 85 87 88
# 89 89 90 90 90 90 93 95 98 98 98 98 99 100 100 100"""
        self.TARGET_OUTPUT = """Student 1: 80 90 70 100 60 90
Student 2: 85 78 93 80 70 98
Student 3: 98 85 100 99 89 90
Student 4: 72 0 78 98 100 65
Student 5: 67 11 28 89 85 90
Student 6: 98 85 87 56 69 22
Student 7: 85 72 95 75 64 88
Student 1 average: 81.67
Student 2 average: 84.00
Student 3 average: 93.50
Student 4 average: 68.83
Student 5 average: 61.67
Student 6 average: 69.50
Student 7 average: 79.83
Lab 1 average: 83.57
Lab 2 average: 60.14
Lab 3 average: 78.71
Lab 4 average: 85.29
Lab 5 average: 76.71
Lab 6 average: 77.57
0 11 22 28 56 60 64 65 67 69 70 70 72 72 75 78 78 80 80 85 85 85 85 85 87 88
89 89 90 90 90 90 93 95 98 98 98 98 99 100 100 100"""

    def grade_lab8(self, output):
        return

    def check_code(self, username, rootdir):
        f = open('{0}{1}/{2}'.format(rootdir, username, self.FILENAME))
        contents = f.read()
        f.close()
        scanf_count = contents.count('scanf')

        if scanf_count > 0:
            print("Found {0} scanf() in the source file.".format(scanf_count))
            self.__scores['scanf']['value'] = self.__scores['scanf']['max']
        else:
            self.__scores['scanf']['comment'] = 'Source file did not contain scanf()'

        return

    def grade(self, username, rootdir):
        output_lines = ''
        reporter = Reporter(username, rootdir)
        print("*********************")
        print("Grading {0}".format(username))
        print("*********************")

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/{2}'.format(rootdir, username, self.FILENAME)])

        if self.__compiler.gcc_compile({'-o': '{0}{1}/{2}'.format(rootdir, username, self.EXENAME), '-Wall': ''}) == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())

            if self.__compiler.stderr() == "":  # there were no warnings
                self.__scores['noWarnings']['value'] = self.__scores['noWarnings']['max']
            else:
                print('=== There were -Wall warnings! ===')
                self.__scores['noWarnings']['value'] = 0
                self.__scores['noWarnings']['comment'] = self.__compiler.stderr()

            # Run program with input and timeout
            runner = Runner('{0}{1}/{2}'.format(rootdir, username, self.EXENAME))
            return_code, args_list = runner.run(timeout=3, input=INPUT)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                self.check_code(username, rootdir)
                self.grade_lab8(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute: {0}'.format(
                    runner.error() + runner.stdout() + runner.stderr())
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['Functionality']['comment'] = 'Failed to compile: {0}'.format(
                self.__compiler.stdout() + self.__compiler.stderr())

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username, INPUT, output_lines)
