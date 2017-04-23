import os
import csv

#todo change this
LAB_NUM='Lab11'
DIRLIST = ['./cpsc1111-004/assignments/{0}/'.format(LAB_NUM), './cpsc1111-003/assignments/{0}/'.format(LAB_NUM), './cpsc1111-002/assignments/{0}/'.format(LAB_NUM), './cpsc1111-001/assignments/{0}/'.format(LAB_NUM)]


def parse_grade_report(dir, rootdir):
    filename = '{0}{1}/REPORT'.format(rootdir, dir)
    writer = csv.writer(open('./grades-{0}final.csv'.format(LAB_NUM), 'a+'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if os.path.exists(filename):
        grade = 0
        for line in open(filename, 'r'):
            if 'Final Score' in line:
                num = (line.split('e')[1])
                grade = float(num.split('/')[0])

        print(dir)
        writer.writerow([dir, grade])


for rootdir in DIRLIST:
    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if '.hg' not in dir and 'cache' not in dir and 'store' not in dir and 'data' not in dir:
                parse_grade_report(dir, rootdir)