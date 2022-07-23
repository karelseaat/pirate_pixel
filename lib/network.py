


class WLAN(object):
    """
    This class will emulate the micropython WLAN library
    """
    AP_IF = 1
    STA_IF = 0

    interface = None
    state = False

#   ap name, macaddress ?, wifi channel from 1 to 14 ?, RSSI is ~ decibell,  authmode open-wpa-wep etc, hidden you know !
#   ssid, bssid, channel, RSSI, authmode, hidden
    fakeaps = [
        ("klont", "tolasytodo", 5, 5, 1, 0),
        ("beest", "tolasytodo", 1, 100, 2, 0),
        ("ladida", "tolasytodo", 10, 75, 3, 0)
    ]

    fakeapwifi = {
        'klont':'beestjes',
        'beest': 'wordwatzaai',
        'ladia': 'maximalezaaiheidberijkt',
    }

    ip = '172.0.0.1'
    subnet = '255.255.0.0'
    gateway = '0.0.0.0'
    dns = '172.0.0.1'

    essid = None
    channel = None
    authmode = None
    mode = 0

    def __init__(self, interface):

        self.interface = interface

    def active(self, state=None):
        """
        Will return of set the active state !

        Params: state in int or boolean
        Return None of the current state !

        """
        if state:
            self.state = state
        else:
            return self.state

    def connect(self, ssid, passwd):
        """
        Not sure that this is a great idea, will set state to true

        Params: ssid and password
        Return: None

        """
        if ssid not in self.fakeapwifi:
            # print("ssid not in the list")
            self.state = False
            self.mode = 0
            return

        # print("ok ssid must in the list !")
        self.mode = 5
        self.state = self.fakeapwifi[ssid] == passwd


    def disconnect(self):
        """
        Will set the state to false ?

        Params: None
        Return: None

        """
        self.state = False
        # state to false only ?

    def scan(self):
        """
        Will return a list with fake aps in the case of real micropython it will return real aps that are close by

        Params: None
        Return: a list of aps/tuples

        """
        return self.fakeaps

    def status(self):
        """
        Returns the status of the connection of the wifi, normaly from 0 to 5

        Params: None
        Return: a 5 or 0 ?

        """
        return self.state

    def isconnected(self):
        """
        Will connect the state or isconnected ?

        Params: None
        Return: the state ?

        """
        # print(self.state, self.mode)
        return self.state

    def ifconfig(self, params=None):
        """
        Set of get the interface config params., like eth0 interface of wifi interface, only ip netmask ect

        Params: params =  name of the prameter to set (params indicates multyple prameters ?!?!)
        Return: if there are no parameters set return the params. (ip, subnet, gateway, dns)

        """
        if params:
            self.ip = params[0]
            self.subnet = params[1]
            self.gateway = params[2]
            self.dns = params[3]
        else:
            return (self.ip, self.subnet, self.gateway, self.dns)

    def config(self, param):
        """
        Returns the config of the wifi based in the param to ask.

        Params: string (essid, channel, authmode, hidden, mac)
        Return: the essid or the channel or the authmode or the hidden bool or even the mac address !

        """
        if param == 'essid':
            return self.essid
        if param == 'channel':
            return self.channel
        if param == 'authmode':
            return self.authmode
        if param == 'hidden':
            return False
        if param == 'mac':
            return "Truth never."
