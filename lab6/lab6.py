from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter

FILENAME = 'factorial_broken.c'
EXENAME = 'lab6'


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'Functionality':            {'value': 0, 'max': 65, 'comment': ''},
            'Answers':                  {'value': 0, 'max': 25, 'comment': ''},
            'Formatting':               {'value': 0, 'max': 10, 'comment': ''},

        }

    def grade_lab6(self, output):
        # Check for correctness of output
        flag = 0
        for line in output:
            if "segmentation" not in line and "fault" not in line and '120' in line:
                self.__scores['Functionality']['value'] = self.__scores['Functionality']['max']
                flag = 1
        if flag == 0:
            self.__scores['Functionality']['comment'] = 'Program execution was not correct'

        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/{2}'.format(rootdir, username, FILENAME)])

        if self.__compiler.gcc_compile({'-o': '{0}{1}/{2}'.format(rootdir, username, EXENAME), '-Wall': ''}) == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            # Run program with input and timeout
            runner = Runner('{0}{1}/{2}'.format(rootdir, username, EXENAME))
            return_code, args_list = runner.run(timeout=3, input=['5'])
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.grade_lab6(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['Functionality']['comment'] = 'Failed to compile'

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username)
