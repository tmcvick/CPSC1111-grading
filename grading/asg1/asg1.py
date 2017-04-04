from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter

FILENAME = 'mastermind.c'
EXENAME = 'asg1'


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'Functionality':            {'value': 0, 'max': 70, 'comment': ''},
            'InvalidInput':             {'value': 0, 'max': 5, 'comment': ''},
            'Formatting':               {'value': 0, 'max': 10, 'comment': ''},
            'noWarnings':               {'value': 0, 'max': 5, 'comment': ''},
            'algorithm':                {'value': 0, 'max': 5, 'comment': ''},
            'estimation':               {'value': 0, 'max': 5, 'comment': ''}
        }

        self.INPUT = ['royg', 'ryog', 'royb', 'boyg']
        self.SEARCH = ['bbbe', 'bwwe', 'bbwe', 'youguessedit']
        self.INVALID_INPUT = ['royg', 'groh', 'ggoy', 'ryog', 'royb', 'boyg']
        self.INVALID_SEARCH = ['bbbe', 'roygb', 'roygb', 'bwwe', 'bbwe', 'youguessedit']

    def grade_asg1(self, output):
        # Check for correctness of output
        flag = 0
        for line in output:
            if self.SEARCH[flag] in line:
                flag += 1
            if flag == 3:
                break
        if flag == 3:
            self.__scores['Functionality']['value'] = self.__scores['Functionality']['max']
        else:
            self.__scores['Functionality']['comment'] = 'Did not find output in correct order'

        return

    def grade_invalid(self, output):
        flag = 0
        for line in output:
            if self.INVALID_SEARCH[flag] in line:
                flag += 1
            if flag == 5:
                break
        if flag == 5:
            self.__scores['InvalidInput']['value'] = self.__scores['InvalidInput']['max']
        else:
            self.__scores['InvalidInput']['comment'] = 'Did not find catch invalid input'

        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)
        output_lines = ""
        invalid_output_lines = ""

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/{2}'.format(rootdir, username, FILENAME)])

        if self.__compiler.gcc_compile({'-o': '{0}{1}/{2}'.format(rootdir, username, EXENAME), '-Wall': ''}) == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            if self.__compiler.stderr() == "":  # there were no warnings
                self.__scores['noWarnings']['value'] = self.__scores['noWarnings']['max']
            else:
                print('=== There were -Wall warnings! ===')
                self.__scores['noWarnings']['value'] = 0
                self.__scores['noWarnings']['comment'] = self.__compiler.stderr()

            # Run program with input and timeout
            runner = Runner('{0}{1}/{2}'.format(rootdir, username, EXENAME))
            return_code, args_list = runner.run(timeout=3, input=self.INPUT)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower().replace(" ", "") for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.grade_asg1(output_lines)
                return_code, args_list = runner.run(timeout=3, input=self.INVALID_INPUT)
                if return_code == 0:
                    print('=== Execution Success ===\n')
                    print(runner.stdout())
                    invalid_output_lines = [line.lower().replace(" ", "") for line in
                                    runner.stdout().split('\n')]  # Split, Strip, and Normalize the output.
                    self.grade_invalid(invalid_output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['Functionality']['comment'] = 'Failed to compile'

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username, self.INPUT, output_lines, self.INVALID_INPUT, invalid_output_lines)
