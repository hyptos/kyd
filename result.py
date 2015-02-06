from __future__ import print_function
import csv
import os
from providerGD import ProviderGD


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
        spamreader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        nb = 0
        ip = None
        lat = None
        lon = None
        ville = None
        pays = None
        for row in spamreader:
            if len(row) > 1:
                ip = row[0]
                lat = row[1]
                lon = row[2]
                ville = row[3]
                pays = row[4]
                cloud = row[5]
                interface = row[6]
                start_time = row[7]
                size = row[8]
                upload = row[9]
                download = row[10]
                try:
                    tab[cloud, size, interface, "up"].append(upload)
                    tab[cloud, size, interface, "dl"].append(download)
                except KeyError:
                    tab[cloud, size, interface, "up"] = [upload]
                    tab[cloud, size, interface, "dl"] = [download]
                all_download += float(download)
                all_upload += float(upload)
                #print ('%s\t%s\t%s' % (start_time, upload, download))
                nb += 1

        moy = []
        for test in tab:
            i = 0
            res = 0
            for val in tab[test]:
                i += 1
                res += float(val)
            res = res/i
            moy.append((ip, lat, lon, ville, pays, test[0], test[1], test[2], test[3], res))

    print (moy)


p = ProviderGD()
drive_service = p.getConnexion()
tutu = p.retrieve_all_files(drive_service,'tpjunit.pdf')


