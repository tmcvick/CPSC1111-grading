from grading.compiler import Compiler
from grading.runner import Runner
from grading.reporter import Reporter

FILENAME = 'lab7.c'
EXENAME = 'lab7'
LOOP_PER = 5
FUNC_PER = 2
INPUT = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '12', '35', '53', '32', '42', '12']


class Script:
    __compiler = None

    # This is your rubric
    def __init__(self):
        self.__compiler = None

        self.__scores = {
            'Functionality':            {'value': 0, 'max': 50, 'comment': ''},
            'loops':                    {'value': 0, 'max': 25, 'comment': ''},
            'noWarnings':               {'value': 0, 'max': 5, 'comment': ''},
            'scanf':                    {'value': 0, 'max': 5, 'comment': ''},
            'rand()':                   {'value': 0, 'max': 5, 'comment': ''},
            'Formatting':               {'value': 0, 'max': 10, 'comment': ''}
        }
        self.SEARCH = ['8', '50', '24', '9', '31', '23', '45', '29', '24', '10', '41', '16', '43', '43', '38', '4', '28',
                  '30', '41', '13', '42', '45', '8094']

    def grade_lab7(self, output):
        # Check for correctness of output
        found = []
        conversion_score = 0
        length_search = len(self.SEARCH) - 4
        flag = {
            '8':1, '50':1, '24':0, '9':1, '31':1, '23':1, '45':0, '29':1, '10':1, '41':0, '16':1, '43':0, '38':1, '4':1, '28':1,
            '30':1, '13':1, '42':1, '8094':1
        }
        for line in output:
            for target in self.SEARCH:
                if line.find(target) > -1 and (target not in found):
                    flag[target] += 1

                    if flag[target] > 0:
                        print("found {0}".format(target))
                        found.append(target)
                        conversion_score += FUNC_PER
                        flag[target] += 1
            if len(found) == length_search:
                break
        for target in found:
            if target in self.SEARCH:
                self.SEARCH.remove(target)

        self.__scores['Functionality']['value'] += conversion_score
        #self.__scores['Functionality']['comment'] += "NOT FOUND: {0}".format(self.SEARCH)

        if conversion_score > 0:
            self.__scores['Functionality']['value'] += 12

        return

    def check_code(self, username, rootdir):
        f = open('{0}{1}/lab7.c'.format(rootdir, username))
        contents = f.read()
        f.close()
        for_count = contents.count('for')
        scanf_count = contents.count('scanf')
        rand_count = contents.count('rand')

        if for_count >= 5:
            print("Found {0} for loops in the source file.".format(for_count))
            self.__scores['loops']['value'] = self.__scores['loops']['max']
        elif for_count > 0:
            print("Found {0} for loops in the source file.".format(for_count))
            self.__scores['loops']['value'] = for_count * LOOP_PER
            self.__scores['loops']['comment'] = 'Source file did not contain enough for loops'
        else:
            self.__scores['loops']['comment'] = 'Source file did not contain enough for loops'

        if scanf_count > 0:
            print("Found {0} scanf() in the source file.".format(scanf_count))
            self.__scores['scanf']['value'] = self.__scores['scanf']['max']
        else:
            self.__scores['scanf']['comment'] = 'Source file did not contain scanf()'

        if rand_count > 0:
            print("Found {0} rand() in the source file.".format(rand_count))
            self.__scores['rand()']['value'] = self.__scores['rand()']['max']
        else:
            self.__scores['rand()']['comment'] = 'Source file did not contain rand()'

        return

    def grade(self, username, rootdir):
        output_lines = ''
        reporter = Reporter(username, rootdir)
        print("*********************")
        print("Grading {0}".format(username))
        print("*********************")

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
            return_code, args_list = runner.run(timeout=3, input=INPUT)
            if return_code == 0:
                print('=== Execution Success ===\n')
                print(runner.stdout())
                output_lines = [line.lower() for line in runner.stdout().split('\n')]   # Split, Strip, and Normalize the output.
                self.check_code(username, rootdir)
                self.grade_lab7(output_lines)
            else:
                print('!!! Execution Failed - {0} !!!'.format(runner.error()))
                print(runner.stderr())
                self.__scores['Functionality']['comment'] = 'Program failed to execute: {0}'.format(runner.error() + runner.stdout() + runner.stderr())
        else:
            print('!!! Compilation Failed !!!')
            print(self.__compiler.stdout() + self.__compiler.stderr())
            self.__scores['Functionality']['comment'] = 'Failed to compile: {0}'.format(self.__compiler.stdout() + self.__compiler.stderr())

        self.__compiler.clear()
        reporter.report_scores(self.__scores, username, INPUT, output_lines)
