__author__ = 'sherry.zheng'
import random
import copy
import linecache
import json

from argparse import ArgumentParser


def gen(filename, count, prot):
    temp = [
        {
            "status": "online",
            "slice": -1,
            "protocol": "tcp",
            "name": "app1",
            "tags": [],
            "params": [],
            "mode": "server_port",
            "id": "app1"
        }
    ]

    apps = []
    appt = copy.deepcopy(temp[0])
    num = 0

    try:
        fp = open(filename, 'r')
        for num, line in enumerate(fp):
            pass
        numlist = range(1, num)
        random.shuffle(numlist)
        for i in range(1, count + 1):
            theapp = linecache.getline(filename, numlist[i])
            app = theapp.split(',')
            item = {
                "server_ports": [],
            }
            if len(app) == 3:
                item['server_ports'].append(app[1])
                appt['id'] = str(app[0])
                appt['name'] = str(app[0])
                appt['protocol'] = str(prot)
                appt['params'].append(item)
                apps.append(appt)
            else:
                print app
                print numlist[i]
            appt = copy.deepcopy(temp[0])
            fp.close()
    except IOError as err:
        print ('File error:' + str(err))

    json.dump(apps, open('wellknow_apps.json', 'w+'), indent=4)

if __name__ == '__main__':

    parser = ArgumentParser(description="v1.0")
    parser.add_argument("-c", "--count", type=int, dest='count', help="gen apps count")
    parser.add_argument("-f", "--filename", dest='filename', help="gen wellknow file")
    parser.add_argument("-p", "--protocol", dest='prot', default='tcp')
    args = parser.parse_args()
    gen(args.filename, args.count, args.prot)
