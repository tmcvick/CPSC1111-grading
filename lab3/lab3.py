from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'Header':                   {'value': 0, 'max': 10, 'comment': ''},
            'Functionality':            {'value': 0, 'max': 70, 'comment': ''},
            'noWarnings':               {'value': 0, 'max': 5, 'comment': ''},
            'CommentsBeforeLines':      {'value': 0, 'max': 10, 'comment': ''},
            'AnswerInHeaderComment':    {'value': 0, 'max': 5, 'comment': ''},
    }

    def grade_lab3(self, output, username, rootdir):
        # Check for correctness of output
        flag = 0
        for line in output:
            if "segmentation" not in line and "fault" not in line and '8' in line:
                self.__scores['Functionality']['value'] = self.__scores['Functionality']['max']
                flag = 1
        if flag == 0:
            self.__scores['Functionality']['comment'] = 'Program execution was not correct'

        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)

        # Compile program with flags
        self.__compiler = Compiler(['{0}{1}/lab3.c'.format(rootdir, username)])

        if self.__compiler.gcc_compile({'-o': '{0}{1}/lab3'.format(rootdir, username), '-Wall': ''}) == 0:
            # -Wall errors are sent via stderr. if the compiler returns 0 it succeeded, so any stderr is a warning
            if self.__compiler.stderr() == "":  # there were no warnings
                self.__scores['noWarnings']['value'] = self.__scores['noWarnings']['max']
            else:
                print('=== There were -Wall warnings! ===')
                self.__scores['noWarnings']['value'] = 0
                self.__scores['noWarnings']['comment'] = self.__compiler.stderr()

            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            # Run program with input and timeout
            runner = Runner('{0}{1}/lab3'.format(rootdir, username))
            return_code, args_list = runner.run(timeout=3, input=['4', '4'])
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.grade_lab3(output_lines, username, rootdir)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute'
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['Functionality']['comment'] = 'Failed to compile'

        if int(self.__scores['Functionality']['value']) == 4:
            self.__scores['Functionality']['value'] = 0

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username)
