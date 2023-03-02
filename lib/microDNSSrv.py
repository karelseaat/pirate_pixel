
import socket
from re import match


class MicroDNSSrv:

    def _ipV4StrToBytes(ipStr):
        """
        This will convert a ipv4 string to 4 x bytes.

        Params: A ipv4 string.
        Return: 4 bytes
        """
        parts = ipStr.split('.')
        if len(parts) == 4:
            return bytes([
                int(parts[0]),
                int(parts[1]),
                int(parts[2]),
                int(parts[3])
            ])

    def _getAskedDomainName(packet):
        """
        Get the domain name from the domain name questions

        Params: The packed of bytes
        Return: The domain name, that was asked ?
        """
        queryType = (packet[2] >> 3) & 15
        qCount = (packet[4] << 8) | packet[5]
        if queryType == 0 and qCount == 1:
            pos = 12
            domName = ''
            while True:
                domPartLen = packet[pos]
                if (domPartLen == 0):
                    break
                domName += (
                    ('.' if len(domName) > 0 else '')
                    + packet[pos+1: pos+1+domPartLen].decode()
                )
                pos += 1+domPartLen
            return domName

    def _getPacketAnswerA(packet, ipV4Bytes):
        """
        will compile a packet to send back as an answer to a dns request

        Params: the packet that has the original question in it
        the ipv4 address that the domain now belongs to
        Return: The compiled answer packet
        """
        queryEndPos = 12
        while True:
            domPartLen = packet[queryEndPos]
            if (domPartLen == 0):
                break
            queryEndPos += 1 + domPartLen
        queryEndPos += 5

        return b''.join([
            packet[:2],                 # Query identifier
            b'\x85\x80',                # Flags and codes
            packet[4:6],                # Query question count
            b'\x00\x01',                # Answer record count
            b'\x00\x00',                # Authority record count
            b'\x00\x00',                # Additional record count
            packet[12:queryEndPos],     # Query question
            b'\xc0\x0c',                # Answer name as pointer
            b'\x00\x01',                # Answer type A
            b'\x00\x01',                # Answer class IN
            b'\x00\x00\x00\x1E',        # Answer TTL 30 secondes
            b'\x00\x04',                # Answer data length
            ipV4Bytes                   # Answer data
        ])

    def __init__(self, port=53):
        self._domList = {}
        self.port = port

    def _serverProcess(self):
        """
        This is the main loop that will be called everytime and will handle the incoming questions

        Params: None
        Return: None
        """
        try:
            packet, cliAddr = self._server.recvfrom(256)
            domName = MicroDNSSrv._getAskedDomainName(packet)
        except Exception as e:
            print("timeout dns !:" + str(e))
            return

        if domName:
            domName = domName.lower()
            ipB = self._domList.get(domName, None)
            if not ipB:
                for domChk in self._domList.keys():
                    if domChk.find('*') >= 0:
                        r = domChk.replace('.', r'\.').replace('*', '.*') + '$'
                        if match(r, domName):
                            ipB = self._domList.get(domChk, None)
                            break
                if not ipB:
                    ipB = self._domList.get('*', None)
            if ipB:

                packet = MicroDNSSrv._getPacketAnswerA(packet, ipB)
                if packet:
                    try:
                        self._server.sendto(packet, cliAddr)
                    except Exception as e:
                        print(e)

    def Start(self):
        """
        perhaps this function is not needed, but for not it sets some socket options
        perhaps this could be done in the init

        Params: None
        Return: None
        """
        self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(('0.0.0.0', self.port))
        self._server.setblocking(False)
        self._server.settimeout(0.5)

    def Stop(self):
        """
        Perhaps this could be done in the del method
        it will stop the server

        Params: None
        Return: None
        """
        self._server.close()

    def SetDomainsList(self, domainsList):
        """
        here we will set the list of domains that will be translated

        Params: None
        Return: None
        """
        if domainsList and isinstance(domainsList, dict):
            o = {}
            for dom, ip in domainsList.items():
                if isinstance(dom, str) and len(dom) > 0:
                    ipB = MicroDNSSrv._ipV4StrToBytes(ip)
                    if ipB:
                        o[dom.lower()] = ipB
                        continue
                break
            if len(o) == len(domainsList):
                self._domList = o
                return True
        return False
