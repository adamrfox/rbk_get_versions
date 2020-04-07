#!/usr/local/bin/python3

import sys
import getopt
import requests
import urllib3
urllib3.disable_warnings()

def usage():
    sys.stderr.write("Usage: rbk_get_versions.py [-h]  -i input_fie [-f os_family]\n")
    sys.stderr.write("-h | --help: Prints this message\n")
    sys.stderr.write("-i | --input: Use this file for host/creds (plain textt)\n")
    sys.stderr.write("-f | --find: Only show versions that start with given string\n")
    sys.stderr.write("NOTE: -i or -c if required\n")
    exit(0)

def get_creds_from_file(config):
    hosts = []
    fp = open(config, "r")
    for line in fp:
        line = line.rstrip()
        if not line.startswith("#") and line != "":
            hosts.append(line)
    fp.close()
    return (hosts)

if __name__ == "__main__":
    hosts = []
    find = ""
    optlist, args = getopt.getopt(sys.argv[1:], 'hc:i:f:', ['--help', '--input=', '--find='])
    for opt, a in optlist:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-i', '--input'):
            hosts = get_creds_from_file(a)
        if opt in ('-f', '--find'):
            find = a
    for rubrik_host in hosts:
#        print ('RUBRIK: ' + rubrik_host)
        try:
            data = requests.get('https://' + rubrik_host + '/api/v1/cluster/me/version', verify=False)
        except:
            print (rubrik_host + " : " + sys.exc_info()[0])
            continue
        version_data = data.json()
        version = version_data['version']
        if find == "":
            print (rubrik_host + " : " + version)
        else:
            if version.startswith(find):
                print (rubrik_host + " : " + version)





