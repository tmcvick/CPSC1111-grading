from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter
import re


class Script:

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'conditionals':         {'value': 0, 'max': 60, 'comment': ''},
            'loop':                 {'value': 0, 'max': 20, 'comment': ''},
            'formatting':           {'value': 0, 'max': 10, 'comment': ''},
            'sqrt':                 {'value': 0, 'max': 5, 'comment': ''},
            'invalid':              {'value': 0, 'max': 5, 'comment': ''}
        }
        self.FILE_NAME = '{0}{1}/lab5.c'
        self.EXECUTABLE_NAME = '{0}{1}/lab5'

        # Conversion Test
        self.SINGLE_BOTH = ['540', '23.24', 'even', 'odd']
        self.SINGLE_ODD = ['333', '18.25', 'odd']
        self.SINGLE_EVEN = ['200', '14.14', 'even']
        self.INVALID = ['Invalid input', 'invalid input']
        self.LOOP = ['540', 'even', 'odd', '333', 'odd']

        # Input
        self.SINGLE_BOTH_INPUT = ['540', '0']
        self.SINGLE_ODD_INPUT = ['333', '0']
        self.SINGLE_EVEN_INPUT = ['200', '0']
        self.DOUBLE_INPUT = ['540', '1', '333', '0']
        self.INVALID_INPUT = ['540', '3', '1', '333', '0']

        self.warning_flag = 0


    def grade_lab5(self, rootdir, username):
        f = open(self.FILE_NAME.format(rootdir, username))
        contents = f.read()
        f.close()
        found = contents.count('sqrt(')
        if found > 0:
            print("Found sqrt() in the source file.")
            self.__scores['sqrt']['value'] = self.__scores['sqrt']['max']
        else:
            self.__scores['sqrt']['comment'] = 'Source file did not contain sqrt()'
        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)
        # Compile program with flags
        self.__compiler = Compiler([self.FILE_NAME.format(rootdir, username)])
        if self.__compiler.gcc_compile({'-o': self.EXECUTABLE_NAME.format(rootdir, username), '-Wall': ''}) == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            if self.__compiler.stderr() != "":  # there were warnings
                self.warning_flag = 5
                self.__scores['conditionals']['comment'] += "There were warnings (-5)"

            self.grade_lab5(rootdir, username)

            # Run program with input and timeout
            runner = Runner('./' + self.EXECUTABLE_NAME.format(rootdir, username))
            return_code, args_list = runner.run(input=self.SINGLE_BOTH_INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab5_both(output_lines_no_blanks)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['conditionals']['comment'] = 'Program failed to execute'
            return_code, args_list = runner.run(input=self.SINGLE_EVEN_INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab5_even(output_lines_no_blanks)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['conditionals']['comment'] = 'Program failed to execute'
            return_code, args_list = runner.run(input=self.SINGLE_ODD_INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab5_odd(output_lines_no_blanks)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['conditionals']['comment'] = 'Program failed to execute'
            return_code, args_list = runner.run(input=self.DOUBLE_INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab5_double(output_lines_no_blanks)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['conditionals']['comment'] = 'Program failed to execute'
            return_code, args_list = runner.run(input=self.INVALID_INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in
                                runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab5_invalid(output_lines_no_blanks)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['conditionals']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['conditionals']['comment'] = 'Failed to compile'

        self.__compiler.clear()

        if self.__scores['conditionals']['value'] >= 5:
            self.__scores['conditionals']['value'] -= self.warning_flag
        elif self.__scores['loop']['value'] >= 5:
            self.__scores['loop']['value'] -= self.warning_flag

        reporter.report_scores(self.__scores, username)

    def grade_lab5_both(self, output_lines_no_blanks):

        found = []
        conversion_score = 0
        length_search = len(self.SINGLE_EVEN)

        for line in output_lines_no_blanks:
            for target in self.SINGLE_BOTH:
                if line.find(target) > -1 and target not in found:
                    print("found {0}".format(target))
                    found.append(target)
                    conversion_score += 5
            if len(found) == length_search:
                break
        for target in found:
            self.SINGLE_BOTH.remove(target)
        self.__scores['conditionals']['value'] += conversion_score
        self.__scores['conditionals']['comment'] += "NOT FOUND: {0}".format(self.SINGLE_BOTH)

        print(found)

    def grade_lab5_even(self, output_lines_no_blanks):
        found = []
        conversion_score = 0
        length_search = len(self.SINGLE_EVEN)
        for line in output_lines_no_blanks:
            for target in self.SINGLE_EVEN:
                if line.find(target) > -1 and target not in found:
                    print("found {0}".format(target))
                    found.append(target)
                    conversion_score += 5
            if len(found) == length_search:
                break
        for target in found:
            self.SINGLE_EVEN.remove(target)
        conversion_score += 5
        self.__scores['conditionals']['value'] += conversion_score
        self.__scores['conditionals']['comment'] += "NOT FOUND: {0}".format(self.SINGLE_EVEN)

        print(found)

    def grade_lab5_odd(self, output_lines_no_blanks):
        found = []
        conversion_score = 0
        length_search = len(self.SINGLE_ODD)
        for line in output_lines_no_blanks:
            for target in self.SINGLE_ODD:
                if line.find(target) > -1 and target not in found:
                    print("found {0}".format(target))
                    found.append(target)
                    conversion_score += 5
            if len(found) == length_search:
                break
        for target in found:
            self.SINGLE_ODD.remove(target)
        conversion_score += 5
        self.__scores['conditionals']['value'] += conversion_score
        self.__scores['conditionals']['comment'] += "NOT FOUND: {0}".format(self.SINGLE_ODD)

        print(found)

    def grade_lab5_double(self, output_lines_no_blanks):
        flag = 0
        found = []
        conversion_score = 0
        length_search = len(self.LOOP)
        for line in output_lines_no_blanks:
            for target in self.LOOP:
                if line.find(target) > -1 and (target not in found) or flag == 1:
                    if target == "odd":
                        flag += 1
                    print("found {0}".format(target))
                    found.append(target)
                    conversion_score += 4
            if len(found) == length_search:
                break
        for target in found:
            if self.LOOP.__contains__(target):
                self.LOOP.remove(target)
        self.__scores['loop']['value'] += conversion_score
        self.__scores['loop']['comment'] += "NOT FOUND: {0}".format(self.LOOP)

        print(found)

    def grade_lab5_invalid(self, output_lines_no_blanks):
        flag = 0
        for line in output_lines_no_blanks:
            for target in self.INVALID:
                if line.find(target) > -1:
                    self.__scores['invalid']['value'] = self.__scores['invalid']['max']
                    flag = 1
                    break
        if flag == 0:
            self.__scores['invalid']['comment'] += "Does not catch invalid input"
