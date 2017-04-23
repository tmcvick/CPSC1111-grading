import os
import sys

#using this as a hack to allow for an import of Script where I only need to change it jn one place
sys.path.extend(['/Users/timmcvicker/Classes/CPSC1111'])

#todo change this
from asg2.asg2 import Script

LAB_NUM='PA2'

DIRLIST = ['./cpsc1110-001/assignments/{0}/'.format(LAB_NUM), './cpsc1110-002/assignments/{0}/'.format(LAB_NUM)]
CSV_FILE = './grades-{0}.csv'.format(LAB_NUM)


def run_grading(dir, rootdir):
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

