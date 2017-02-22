from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter
import re


class Script:

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'functionality':        {'value': 0, 'max': 70, 'comment': ''},
            'formatting':           {'value': 0, 'max': 10, 'comment': ''},
            'loops':                {'value': 0, 'max': 10, 'comment': ''},
            'fprintfANDfscanf':     {'value': 0, 'max': 5, 'comment': ''},
            'columns':              {'value': 0, 'max': 5, 'comment': ''}
    }

    __compiler = None
    FILE_NAME = '{0}{1}/lab4.c'
    EXECUTABLE_NAME = '{0}{1}/lab4'

    # Conversion Test
    DECIMAL = '37'
    OCTAL   = '45'
    HEX     = '25'
    SUM     = '58'
    SEARCH  = [DECIMAL, OCTAL, HEX, SUM]
    LOOPS   = ['for', 'while']
    CONVERSION_SCORE_PER = 15


    # Input
    CHAR    = '%'
    INPUT = [CHAR]

    def grade_lab4(self, output, rootdir, username):
        # Check for use of fprintf and fscanf
        f = open(self.FILE_NAME.format(rootdir, username))
        contents = f.read()
        f.close()
        fprintf_count = contents.count('fprintf')
        fscanf_count = contents.count('fscanf')

        print("Found 'fprintf' {0} times in the source file.".format(fprintf_count))
        print("Found 'fscanf' {0} times in the source file.".format(fscanf_count))

        if fprintf_count > 0 and fscanf_count > 0:
            self.__scores['fprintfANDfscanf']['value'] = self.__scores['fprintfANDfscanf']['max']
        else:
            self.__scores['fprintfANDfscanf']['comment'] = \
                'Insufficient use of fprintf/fscanf (-{0})'.format(self.__scores['fprintfANDfscanf']['max'])

        match = re.findall('fprintf\(.*\".*%-?#?-?[1-9]+d.*%-?#?-?[1-9]+o.*%-*#*-*[1-9]*x.*\"', contents)
        if match:
            self.__scores['columns']['value'] = self.__scores['columns']['max']

        # Find the correct hex/decimal/octal representations
        found = []
        conversion_score = 10
        length_search = len(self.SEARCH)
        for line in output:
            for target in self.SEARCH:
                if line.find(target) > -1 and target not in found:
                    print("found {0}".format(target))
                    found.append(target)
                    conversion_score += self.CONVERSION_SCORE_PER
            if len(found) == length_search:
                break
        self.__scores['functionality']['value'] += conversion_score
        print(found)

        # loop for loop
        loop_found = contents.count('while') + contents.count('for')
        if loop_found > 0:
            print("Found a loop in the source file.")
            self.__scores['loops']['value'] = self.__scores['loops']['max']
        else:
            self.__scores['loops']['comment'] = 'Source file did not contain a loop'
        return

    def grade(self, username, rootdir):
        reporter = Reporter(username, rootdir)
        # Compile program with flags
        self.__compiler = Compiler([self.FILE_NAME.format(rootdir, username)])
        if self.__compiler.gcc_compile({'-o': self.EXECUTABLE_NAME.format(rootdir, username), '-Wall': ''}) == 0:
            print('=== Compilation Success ===\n')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            # Run program with input and timeout
            runner = Runner('./' + self.EXECUTABLE_NAME.format(rootdir, username))
            return_code, args_list = runner.run(input=self.INPUT, timeout=3)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                output_lines_no_blanks = filter(lambda x: x != '', output_lines)
                self.grade_lab4(output_lines_no_blanks, rootdir, username)
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
