#!/usr/local/bin/python3

import sys
import getopt
import rubrik_cdm
import urllib3
urllib3.disable_warnings()
from codecs import decode

def usage():
    sys.stderr.write("Usage: rbk_get_versions.py [-h] -c config | -i config [-f os_family\n")
    sys.stderr.write("-h | --help: Prints this message\n")
    sys.stderr.write("-c | --config: Use this file for hosts/creds (encoded)\n")
    sys.stderr.write("-i | --input: Use this file for host/creds (plain textt)\n")
    sys.stderr.write("-f | --find: Only show versions that start with given string\n")
    sys.stderr.write("NOTE: -i or -c if required")
    exit(0)

def get_creds_from_file(config, encoded):
    creds = {}
    with open(config) as fp:
        data = fp.read()
    fp.close()
    if encoded:
        data = decode(bytes(data, 'ascii'), 'uu')
        data = decode(str(data), 'rot13')
        data = data.replace("o'", "")
        lines = data.split('\\a\\a')
    else:
        lines = data.splitlines()
    for x in lines:
        xf = x.split(':')
        if len(xf) != 3:
            continue
        creds[xf[0]] = {'user': xf[1], 'password': xf[2]}
    return(creds)

if __name__ == "__main__":
    creds = {}
    find = ""
    optlist, args = getopt.getopt(sys.argv[1:], 'hc:i:f:', ['--help', '--config=', '--input=', '--find='])
    for opt, a in optlist:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-c', '--config'):
            creds = get_creds_from_file(a, True)
        if opt in ('-i', '--input'):
            creds = get_creds_from_file(a, False)
        if opt in ('-f', '--find'):
            find = a
    for rubrik_host in creds.keys():
#        print ('RUBRIK: ' + rubrik_host)
        try:
            rubrik = rubrik_cdm.Connect(rubrik_host, creds[rubrik_host]['user'], creds[rubrik_host]['password'])
        except rubrik_cdm.exceptions.ApiCallException as e:
            print (rubrik_host + " : " + str(e))
            continue
        version = rubrik.cluster_version(timeout=60)
        if find == "":
            print (rubrik_host + " : " + version)
        else:
            if version.startswith(find):
                print (rubrik_host + " : " + version)





