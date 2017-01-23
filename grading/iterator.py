import os
import sys

#using this as a hack to allow for an import of Script where I only need to change it jn one place
sys.path.extend(['/Users/timmcvicker/Classes/CPSC1111'])

#todo change this
from lab1.lab1 import Script

LAB_NUM='Lab1'

DIRLIST = ['./cpsc1111-004/assignments/{0}/'.format(LAB_NUM), './cpsc1111-003/assignments/{0}/'.format(LAB_NUM), './cpsc1111-002/assignments/{0}/'.format(LAB_NUM), './cpsc1111-001/assignments/{0}/'.format(LAB_NUM)]
CSV_FILE = './grades-{0}.csv'.format(LAB_NUM)


def run_grading(dir, rootdir):
    #todo make sure to change this lab1
    grading_script = Script()
    grading_script.grade(dir, rootdir)


try:
    os.remove(CSV_FILE)
except OSError:
    pass

for rootdir in DIRLIST:
    for subdir, dirs, files in os.walk(rootdir):
        for dir in dirs:
            if '.hg' not in dir and 'cache' not in dir and 'store' not in dir and 'data' not in dir:
                run_grading(dir, rootdir)

