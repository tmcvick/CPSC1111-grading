from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter

FILENAME = 'StPat.c'
EXENAME = 'asg2'


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'functionality':            {'value': 0, 'max': 65, 'comment': ''},
            'noWarnings':               {'value': 0, 'max': 5, 'comment': ''}
        }
        self.INPUT = ['']

    def grade_asg2(self, output):

        return

    def grade(self, username, rootdir):
        print("\n********************************")
        print "************  Grading {0}  ********".format(username)
        print("**********************************\n")
        reporter = Reporter(username, rootdir)
        output_lines = ""

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
            INPUT = {'/Users/timmcvicker/Classes/CPSC1111/grading/asg2/input.txt': ''}
            return_code, args_list = runner.run(timeout=3, args=INPUT)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower().replace(" ", "") for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.grade_asg2(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['functionality']['comment'] = 'Program failed to execute: {0}'.format(runner.stderr() + runner.stdout())
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['functionality']['comment'] = 'Failed to compile: {0}'.format(self.__compiler.stdout() + self.__compiler.stderr())

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username, self.INPUT, output_lines)
