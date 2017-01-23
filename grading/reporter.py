import csv
import os

#todo change this
LAB_NUM='Lab1'

class Reporter:
    __studentReport = None
    __grader = None

    #todo i need to figure out how to export these grades
    def __init__(self, username, rootdir):
        filepath = '{0}{1}/REPORT'.format(rootdir, username)

        try:
            os.remove(filepath)
        except OSError:
            pass

        self.__studentReport = open(filepath, 'w+')

    def write_grade(self, row):
        with open('./grades-{0}.csv'.format(LAB_NUM), 'a+') as csvfile:
            self.__grader = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            self.__grader.writerow(row)

    def report_scores(self, scores, username):
        total = 0
        max_possible = 0
        print("\n======================")
        print("===  Grade Report  ===")
        print("======================\n")

        for criterion, score in scores.items():
            total        += score['value']
            max_possible += score['max']

            print(criterion)
            print(score['value'])

            self.write_grade([username, criterion, score['value']])

            # Submit to student report API
            report_string = criterion + ' test ... {0}/{1}\n\t{2}\n'.format(score['value'], score['max'], score['comment'])
            print(report_string)
            self.__studentReport.write(report_string)

        self.write_grade([username, "total", total])
        self.__studentReport.write('Final Score {0}/{1}'.format(total, max_possible))
        print('Final Score {0}/{1}'.format(total, max_possible))
