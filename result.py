from __future__ import print_function
import csv
import os


def getAllResults():
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".txt"):
                if file.startswith("res"):
                    print(os.path.join(root, file))

def calcAverage():

    all_download = 0
    all_upload = 0
    tab = dict()
    with open('all_results.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ' ,skipinitialspace=True)
        nb = 0
        for row in spamreader:
            if len(row) > 1 :
                start_time = row[0]
                size = row[1]
                upload = row[2]
                download = row[3]
                tab[size] = {upload,download}
                all_download += float(download)
                all_upload += float(upload)
                print ('%s\t%s\t%s' % (start_time, upload, download))
                nb += 1
    print (tab)

calcAverage()

