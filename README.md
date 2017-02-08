# CPSC1111-grading
This repository will be used to grade labs for CPSC1111 at Clemson University.

All python scripts will be written using at least Python 2.7.13.

The grading directory includes scripts that are used for each lab. There are multiple places where the script must be changed depending on which lab is being run.

Each Script class in each lab module will grade an individual lab and export a grading report for an individual student.

The grades are uploaded to the handin bucket, as well as exported into a csv for easy uploading.

#Running the scripts using Bash aliasing
###The relevant aliases in my bash_profile are:

* alias grade="cd /Users/timmcvicker/Classes/CPSC1111-repo; python /Users/timmcvicker/Classes/CPSC1111/grading/iterator.py"

* alias grade_report="cd /Users/timmcvicker/Classes/CPSC1111-repo; python /Users/timmcvicker/Classes/CPSC1111/grading/parser.py"

* alias commit="hg add * --subrepos; hg commit -m 'grading' --subrepos; hg push"

* alias grade_commit="cd /Users/timmcvicker/Classes/CPSC1111-repo/cpsc1111-004; commit; cd ../cpsc1111-003; commit; cd ../cpsc1111-002; commit; cd ../cpsc1111-001; commit"

* alias grade_pull="cd /Users/timmcvicker/Classes/CPSC1111-repo/cpsc1111-004; ./update; cd ../cpsc1111-003; ./update; cd ../cpsc1111-002; ./update; cd ../cpsc1111-001; ./update"

* alias grade_combine="cd /Users/timmcvicker/Classes/CPSC1111-repo; python /Users/timmcvicker/Classes/CPSC1111/grading/combiner.py"

#Workflow
In order to grade labs, the following steps are necessary:

0. Change the paths above to reflect where you have cloned the student repositories

  NOTE: TA's that are only grading one section only need to include the buckets that they are using. I needed to pull all four

1. first run the grade_pull command to update student repositories, making sure not to grade any late labs (handin will indicate that the labs are late whenever i commit)

2. run the grade command to grade labs. This will run the script on each student in all four sections, exporting a csv file at the root level, as well as a REPORT file in the student directory that includes grading comments

3. run the grade_commit command to push the REPORTS to the student buckets

4. Each TA runs the grade_pull command and then grades his/her students formatting by replacing the necessary numbers in the REPORT files.  Add comments under the formatting line, but make sure to replace the 0/10 with the appropriate grade.  **REPLACING IS VERY IMPORTANT** For Example: 10/10

5. Once completed, each TA will run the grade_commit script to push his/her changes

6. re-run the grade_pull command

7. Update reports/csv to reflect absences

8. run the grade_report command to centralize the formatting grades

9. For Canvas grades, run the grade_combine alias to combine the new csv into the canvas gradebook csv

10. upload csv and REPORTS, if necessary
