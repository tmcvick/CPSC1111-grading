from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter
import sys
import os

scores = {
        'Formatting':               {'value': 0, 'max': 10, 'comment': ''},
        'Functionality':            {'value': 0, 'max': 70, 'comment': ''},
        'noWarnings':               {'value': 0, 'max': 5, 'comment': ''},
        'OutputFile':               {'value': 0, 'max': 5, 'comment': ''},
        'AnswerInHeaderComment':    {'value': 0, 'max': 5, 'comment': ''},
        'fprintf':                  {'value': 0, 'max': 5, 'comment': ''}
    }


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = scores

    def grade_lab3(self, output, username, rootdir):
        # Check for submitted output file
        if os.path.isfile('{0}{1}/output.txt'.format(rootdir, username)):
            self.__scores['OutputFile']['value'] = scores['OutputFile']['max']
        else:
            self.__scores['OutputFile']['comment'] = 'No output.txt found! (-{0})'.format(scores['OutputFile']['max'])

        # Check for use of fprintf
        f = open('{0}{1}/lab3.c'.format(rootdir, username))
        contents = f.read()
        f.close()
        fprintf_count = contents.count('fprintf')
        print("Found 'fprintf' {0} times in the source file.".format(fprintf_count))

        if fprintf_count >= 1:
            self.__scores['fprintf']['value'] = scores['fprintf']['max']
        else:
            self.__scores['fprintf']['comment'] = 'Insufficient use of fprintf (-{0})'.format(scores['fprintf']['max'])

        # Check for correctness of output
        output_no_whitespace = [line.replace(' ', '') for line in output]
        functionality_score = 0

        targets = ['intVar1=4', 'intVar2=3', 'intVar3=3', 'intVar4=5, ''exp1=24', 'exp2=2', 'exp3=5', 'exp4=1']
        found = []

        for line in output_no_whitespace:
            for target in targets:
                if line.find(target) > -1:
                    found.append(target)
                    functionality_score += scores['Functionality']['max'] / len(targets)
                    break
            if functionality_score == scores['Functionality']['max']:
                break

        self.__scores['Functionality']['value'] = functionality_score
        if len(found) < len(targets):
            self.__scores['Functionality']['comment'] = \
                "Output incomplete, only found {0}(-{1})".format(found, scores['Functionality']['max'] - functionality_score)

        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/lab3.c'.format(rootdir, username)])

        if self.__compiler.gcc_compile({'-o': '{0}{1}/lab3'.format(rootdir, username), '-Wall': ''}) == 0:
            # -Wall errors are sent via stderr. if the compiler returns 0 it succeeded, so any stderr is a warning
            if self.__compiler.stderr() is not '':  # there were warnings
                print('=== There were -Wall warnings! ===')
                self.__scores['noWarnings']['value'] = 0
                self.__scores['noWarnings']['comment'] = self.__compiler.stderr()
            else:
                self.__scores['noWarnings']['value'] = scores['noWarnings']['max']

            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            # Run program with input and timeout
            runner = Runner('{0}{1}/lab3'.format(rootdir, username))
            return_code, args_list = runner.run(timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.grade_lab3(output_lines, username, rootdir)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['functionality']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['functionality']['comment'] = 'Failed to compile'

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username)
