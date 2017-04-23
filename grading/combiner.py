import os
import csv

#todo change this
LAB_NUM='Lab11'
LAB_NUM_PREV='Lab10'
found = []
with open('./grades-{0}final.csv'.format(LAB_NUM), 'r+') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    final = csv.writer(open('./gradebook{0}.csv'.format(LAB_NUM), 'a+'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer = csv.reader(open('./gradebook{0}.csv'.format(LAB_NUM_PREV), 'r+'), delimiter=',', quotechar='|',
                        quoting=csv.QUOTE_MINIMAL)
    final.writerow(writer.next())
    for read_row in reader:
        username = read_row[0]
        writer = csv.reader(open('./gradebook{0}.csv'.format(LAB_NUM_PREV), 'r+'), delimiter=',', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
        for write_row in writer:
            if username in write_row[4] and username not in found:
                #todo add the previous column (lab7 is write_row[8])
                final.writerow([write_row[0], write_row[1], write_row[2], write_row[3], write_row[4], write_row[5], write_row[6], write_row[7], write_row[8], write_row[9], write_row[10], read_row[1]])
                found.append(username)

