#!/usr/bin/env python
from lib.filehelper import filehelper
import sys, getopt
import hashlib



allconfigs = {
    'first':{'TESTAPS':False, 'CONNS':{'ConnectAThing': 'on', 'AdaFruit': 'on', 'API': 'on', 'CustomMqtt': 'on'}, 'APS':[{'WIFISSID':'meh', 'WIFIPASSWD':'efeef', 'TESTCONNECT': 0, 'USETHIS': False}, {'WIFISSID':'LEL', 'WIFIPASSWD':'Nope', 'TESTCONNECT': 0, 'USETHIS': False}],'MQTTUSERNAME':'testingusername','MQTTADDRESS':'10.10.10.10','MQTTPASSWORD':'geenpasswd', 'ADMINPASSWD':'aaps', 'ADAUSERNAME':'someadauser', 'ADAKEY':'not_a_real_key', "APIAUTHASSWORD":"klont"},
    'KLONT':{'CONNS': {'ConnectAThing': '', 'AdaFruit': '', 'API': 'on', 'CustomMqtt': ''}, 'APS':[], 'MQTTUSERNAME':'CCCP','MQTTADDRESS':'666.10.666.10','MQTTPASSWORD':'', 'ADMINPASSWD': 'efergergerh', 'ADAUSERNAME': 'someadauser', 'ADAKEY':'not-a-real-key'}
}

def writefile(configname):
    config = allconfigs[configname]
    m = hashlib.sha256()
    m.update(str.encode(config['ADMINPASSWD']))
    config['ADMINPASSWD'] = m.hexdigest()
    filehelper("./config.json").open().updatedict(config).writedict().close()


def showhelp():
    print('genrateconfig.py -c configoption -s configoption -h  -a')
    print('-c configoption, will generate a config file acording to the configoption')
    print('-s configoption, will print the config json acording to the configoption')
    print('-a, will print a list of all avalable configoptions')
    print('-h, will print this help')

def main(argv):

    try:
        opts, args = getopt.getopt(argv,"hac:s:",["cnumber=","snumber="])
    except getopt.GetoptError:
        print('genrateconfig.py -c confignumber -s show confignumber -h this help -a show all configs')
        sys.exit(2)

    if not opts:
        showhelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            showhelp()
            sys.exit()
        elif opt == '-a':
            print("config keys present:")
            for value in allconfigs.keys():
                print(value)

            sys.exit()
        elif opt in ("-c", "--cnumber") and arg in allconfigs:
            writefile(arg)
        elif opt in ("-s", "--snumber") and arg in allconfigs:
            print(allconfigs[arg])
        else:
            print("If you see this nothing happened since you chose a wrong option of config, try: genrateconfig.py -h")



if __name__ == "__main__":
   main(sys.argv[1:])
