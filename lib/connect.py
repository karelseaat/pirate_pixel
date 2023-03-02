
import time
from lib.network import WLAN

class Connect(object):
    """
    This class will test if you are connected to the internet or not
    It would be nice if this class extends the network class
    """

    Internetconnected = False
    testtimer = 0
    network = None
    address = "thisissomefakeddress"
    static = {}
    newversion = []
    config = None

    refresh_token = ""
    access_token = ""
    connected_to = ""
    expires_in = 0
    expire_refresh_timer = 0


    def __init__(self, net_if=None, backend_url="example.com",backend_port=80):
        self.change_if(net_if)
        self.backend_url = backend_url
        self.backend_port = backend_port

    def set_config(self, view):
        self.config = view.tempconfig.content


    def isconnected(self):
        return self.network.isconnected()

    def get_connected_ssid(self):
        if self.network.mode != 5:
            return {}
        for value in self.config['APS']:
            if value['USETHIS']:
                return value

        return 'lelelele'

    def get_connected_to(self):
        return self.connected_to

    def wifi_connect(self):

        if self.network and self.config and 'APS' in self.config and self.config['APS']:
            for value in self.config['APS']:

                if value['USETHIS']:

                    # self.connect(value['WIFISSID'], value['WIFIPASSWD'])
                    self.network.connect(value['WIFISSID'], value['WIFIPASSWD'])
                    countconnect = 0
                    while not self.network.isconnected() and countconnect < 5:
                        countconnect += 1
                        time.sleep(0.5)

                    if self.network.isconnected():
                        self.connected_to = value['WIFISSID']

                    return

                    # if not self.network.isconnected():
                    #     print('is connected ', value)
                    #     # stel netwerk in zodat het zelf een ap is.
                    #     pass




    # def test_wifi(self):
    #
    #     accespoints = []
    #
    #     if self.network and self.config and 'APS' in self.config and self.config['APS']:
    #
    #         for value in self.config['APS']:
    #             if value['TESTCONNECT'] == 1:
    #                 self.network.connect(value['WIFISSID'], value['WIFIPASSWD'])
    #
    #                 countconnect = 0
    #                 while not self.network.isconnected() and countconnect < 5:
    #                     countconnect += 1
    #                     time.sleep_ms(500)
    #
    #                 if self.network.isconnected():
    #                     value['TESTCONNECT'] = 0
    #                 else:
    #                     value['TESTCONNECT'] = 2



    def connect(self, ssid, passwd):
        """
        This will try to connect to an accespoint, via the network class and only if the connection mode is 0

        Params: Th ssid of the accespoint and the password of the accespoint !
        Return: None
        """

        self.network.connect(ssid, passwd)

        # return self.network.status()

    def change_if(self, net_if=None):
        """
        This will chnage the connection interface and the connection mode from accting like an accespoibnt to a accespoint client and back.

        Params: the interface that you want to use
        Return: None
        """
        if net_if is not None:
            self.network = WLAN(net_if)
            # self.mode = net_if

    def ip_config(self):
        """
        will return the interface config from the network instance

        Params: None
        Return: a tuple with (ip, subnet, gateway, dns)
        """
        return self.network.ifconfig()

    def network_config(self, name):
        """
        will return the wifi config.
        The info it will return will depend on the name parameter.
        essid, channel, authmode, hidden, mac

        Params: name
        Return: essid or channel or authmode or hidden or mac

        """

        return self.network.config(name)


    def get_versions(self):
        """
        Will get the latest version from the api backend, later moet er ook worden gecontroleerd of de versies van het apperaat
        updatodate zijn en op basis daarvan een true of false teruggeven !

        Params: None
        Return: ?
        """
        if self.network and self.network.isconnected():
            # DISABLEONBUILD 1
            import requests
            #ENABLEONBUILD 1
            #import urequests as requests
            mac = self.network_config('mac')
            try:
                requestresult = requests.get('http://%s:%s/get_latest_version/%s/%s/%s/%s' % (self.backend_url, self.backend_port, self.static['name'], self.static['soft_version'], self.static['hard_version'], mac))
            except Exception as e:
                print(e)
                del requests
                return 1

            del requests
            if requestresult.status_code == 200:
                text = requestresult.text
                if text:
                    return text
                else:
                    return 3
            else:
                return 2
        else:
            return 0

    def update_hardware(self, buttons):
        import requests, json
        if self.network and self.network.isconnected() and self.refresh_token:
            try:
                requestresult = requests.post('http://%s:%s/devcomunication' % (self.backend_url, self.backend_port), headers = {'Authorization': "Bearer " + self.access_token, 'content-type': "application/json"}, data = json.dumps({'buttons': buttons}))
            except Exception as e:
                return 'nope'

            if requestresult.status_code == 200:
                return requestresult.text
            else:
                return 'nope'
        return 'nope'

    def send_customer_message(self, message, mesgid):
        # DISABLEONBUILD 1
        import requests
        #ENABLEONBUILD 1
        #import urequests as requests
        if self.network and self.network.isconnected() and self.refresh_token:
            try:
                requestresult = requests.get('http://%s:%s/sendmessage/%s/%s' % (self.backend_url, self.backend_port, message, mesgid), headers={'Authorization': "Bearer " + self.access_token})
            except Exception as e:
                print(e)
                del requests
                return 1, 0

            del requests
            if requestresult.status_code == 200:
                text = requestresult.text.split(',')
                if text:
                    return text
                else:
                    return 3, 0
            else:
                return 2, 0
        else:
            return 0, 0


    def check_expire_refresh(self):
        # DISABLEONBUILD 1
        import requests
        #ENABLEONBUILD 1
        #import urequests as requests


        if self.network and self.network.isconnected() and self.refresh_token:
            try:
                requestresult = requests.post('http://%s:%s/token/refresh' % (self.backend_url, self.backend_port), headers={'Authorization': "Bearer " + self.refresh_token})
                self.handle_tokens(requestresult)
            except Exception as e:
                print(e)
                del requests
                return 0

        del requests

    def login_user(self, postjson):
        if self.network and self.network.isconnected():
            # DISABLEONBUILD 1
            import requests, json
            #ENABLEONBUILD 1
            #import urequests as requests

            try:
                requestresult = requests.post('http://%s:%s/login' % (self.backend_url, self.backend_port), headers = {'content-type': 'application/json'}, data = postjson)
            except Exception as e:
                print(e)
                del requests
                return 0

            del requests

            if requestresult.status_code == 200:
                return self.handle_tokens(requestresult)
            else:
                return 1
        else:
            return 2
    def backend_loggedin(self):
        return bool(self.refresh_token) and bool(self.access_token)
            # expires_in = "" deze moet uiteindelijk ook worden gechecked of die niet expired is !

    def handle_tokens(self, requestresult):

        if '{' in requestresult.text and '}' in requestresult.text:

            # DISABLEONBUILD 1
            import  json
            #ENABLEONBUILD 1
            #import ujson as json

            dictresult =  json.loads(requestresult.text)
            if 'refresh_token' in dictresult:
                self.refresh_token = dictresult['refresh_token']
            if 'access_token' in dictresult:
                self.access_token = dictresult['access_token']
            if 'expires_in' in dictresult:
                self.expires_in = int(float(dictresult['expires_in']))
            del json
            if 'message' in dictresult:
                return dictresult['message']

        else:
            del json
            return requestresult.text

    def register_user(self, postjson):
        if self.network and self.network.isconnected():
            # DISABLEONBUILD 1
            import requests, json
            #ENABLEONBUILD 1
            #import urequests as requests

            try:
                requestresult = requests.post('http://%s:%s/registration' % (self.backend_url, self.backend_port), headers = {'content-type': 'application/json'}, data = postjson)
            except Exception as e:
                print(e)
                del requests
                return 0

            del requests

            if requestresult.status_code == 200:

                return self.handle_tokens(requestresult)
            else:
                return 1
        else:
            return 2

    def deregister_connect_a_thing(self):
        if self.network and self.network.isconnected():
            # DISABLEONBUILD 1
            import requests
            #ENABLEONBUILD 1
            #import urequests as requests

            mac = self.network_config('mac')

            try:
                requestresult = requests.delete('http://%s:%s/registerdevice' % (self.backend_url, self.backend_port), headers={'Authorization': "Bearer " + self.access_token, 'content-type': 'application/json'}, data = '{"mac":"' +  mac + '"}')
            except Exception as e:
                print(e)
                del requests
                return 0

            del requests

            if requestresult.status_code == 200:
                return requestresult.text
            else:
                return 1
        else:
            return 2


    def register_connect_a_thing(self):
        """
        Will register a device if you login via this / a device this way, what to do about spoofing this way ?

        Params: postjson is the postdata of the login form, it will contain the password and the username of the user that is known at the api backend !
        Return: A true if it worked out and a false of things whent wrong !
        """
        if self.network and self.network.isconnected():
            # DISABLEONBUILD 1
            import requests
            #ENABLEONBUILD 1
            #import urequests as requests

            mac = self.network_config('mac')

            try:
                requestresult = requests.post('http://%s:%s/registerdevice' % (self.backend_url, self.backend_port), headers={'Authorization': "Bearer " + self.access_token, 'content-type': 'application/json'}, data = '{"mac":"' +  mac + '"}')
            except Exception as e:
                print(e)
                del requests
                return 0

            del requests

            if requestresult.status_code == 200:
                return requestresult.text
            else:
                return 1
        else:
            return 2

    def set_version(self, static):
        self.static = static

    def update(self):
        """
        this is the update loop of this class it will call the test functions

        Params: None
        Return: None
        """
        timestamp = time.time()
        if timestamp > self.testtimer:
            self.testtimer = timestamp + 60

            temp = self.get_versions()


            if isinstance(temp, str):
                self.newversion = [bool(int(item)) for item in temp.strip().replace('"', '').split(',')]
                self.Internetconnected = True
            else:
                self.newversion = 0,0

            if isinstance(temp, int):
                self.Internetconnected = (temp > 2)

        if timestamp > self.expire_refresh_timer:
            self.expire_refresh_timer = timestamp + (self.expires_in - 60)
            self.check_expire_refresh()


    def get_version(self):

        return self.newversion

    def getmodes(self):
        """
        this will return the modes, like connectedto website
        and connectable to dns a structure to display the status on the pages

        Params: None
        Return: a dict of mode items !
        """
        if self.network:
            return {
                'mode': self.network.mode,
                'connected': self.network.isconnected(),
                'internet': self.Internetconnected
            }
        return {}

    def get_accespoints(self):
        """
        This will get all the accespoint that are in range !

        Params: None
        Return: A list of accespoints that are in range.
        """
        if self.network.mode == 0:
            return { ap[0]:ap[0] for ap in self.network.scan() }
        return {}


if __name__ == '__main__':
    connect = Connect()
    while True:
        time.sleep(1)
        connect.update()
