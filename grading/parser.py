import os
import csv

#todo change this
LAB_NUM='Lab5'
DIRLIST = ['./cpsc1111-004/assignments/{0}/'.format(LAB_NUM), './cpsc1111-003/assignments/{0}/'.format(LAB_NUM), './cpsc1111-002/assignments/{0}/'.format(LAB_NUM), './cpsc1111-001/assignments/{0}/'.format(LAB_NUM)]


def parse_grade_report(dir, rootdir):
    filename = '{0}{1}/REPORT'.format(rootdir, dir)
    with open('./grades-{0}.csv'.format(LAB_NUM), 'r+') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(open('./grades-{0}final.csv'.format(LAB_NUM), 'a+'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if os.path.exists(filename):
            grade = 0
            found = []
            for line in open(filename, 'r'):
                if 'Final Score' in line:
                    num = (line.split('e')[1])
                    grade = float(num.split('/')[0])
            for line in open(filename, 'r'):
                #todo change this
                if 'formatting test' in line:
                    word = line.split('...')[1]
                    found.append(float(word.split('/')[0]))
                    if len(found) == 1:
                        for row in reader:
                            if dir == row[0] and row[1] == 'total':
                                functionality_score = row[2]
                                total_score = float(functionality_score) + found[0]
                                if total_score != grade:
                                    print('********** {0}{1} grade incorrect ***********'.format(rootdir, dir))
                                writer.writerow([dir, grade])


for rootdir in DIRLIST:
    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if '.hg' not in dir and 'cache' not in dir and 'store' not in dir and 'data' not in dir:
                parse_grade_report(dir, rootdir)