import unittest, os

if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.microDNSSrv import MicroDNSSrv
else:
    from lib.microDNSSrv import MicroDNSSrv

class TestMicroDnsSrv(unittest.TestCase):

    def test_stringtoip(self):
        listobytes = MicroDNSSrv._ipV4StrToBytes("10.65.8.111")
        self.assertTrue(len(listobytes) == 4)

    def test_setdomainlist(self):
        dns = MicroDNSSrv()
        test = dns.SetDomainsList({"*": "192.168.4.1"})

        self.assertTrue(dns._domList['*'] == b'\xc0\xa8\x04\x01')

    def test_StartStop(self):
        dns = MicroDNSSrv(port=5353)
        dns.Start()
        self.assertFalse(dns._server._closed)
        dns.Stop()
        self.assertTrue(dns._server._closed)
    #
    def test_getpacketanswer(self):
        somepacket = b'\x0e\x18\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x03www\x02nu\x02nl\x00\x00\x1c\x00\x01\x00\x00)\x04\xb0\x00\x00\x00\x00\x00\x00'
        ipv4bytes = b'\nA\x08o'
        self.assertTrue(MicroDNSSrv._getPacketAnswerA(somepacket, ipv4bytes) == b'\x0e\x18\x85\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03www\x02nu\x02nl\x00\x00\x1c\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x1e\x00\x04\nA\x08o')

    def test_askdomainlist(self):
        somepacket = b'\x0e\x18\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x03www\x02nu\x02nl\x00\x00\x1c\x00\x01\x00\x00)\x04\xb0\x00\x00\x00\x00\x00\x00'
        domainname = MicroDNSSrv._getAskedDomainName(somepacket)
        self.assertTrue(domainname == 'www.nu.nl')
