import unittest, os

if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.websettings import websettings
else:
    from lib.websettings import websettings


class TestWebSettings(unittest.TestCase):

    def notrun(self):
        print("NOOOOO")

    def setUp(self):
        self.webset = websettings()

    def tearDown(self):
        self.webset = None

    def test_urlparse(self):
        result = self.webset.urlparse("http://www.peterbla.nl:8080/aap/noot/mies?aap=324&lol=432")
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[1]), 5)
        self.assertTrue('aap' in result[0])
        self.assertTrue('lol' in result[0])
        self.assertTrue('noot' in result[1])
        self.assertTrue('aap' in result[1])
        self.assertTrue('mies' in result[1])

    def test_splitparams(self):
        result = self.webset.splitparams("aap=324&lol=432")
        self.assertTrue('aap' in result)
        self.assertTrue('lol' in result)

        self.assertTrue(result['lol'] == "432")
        self.assertTrue(result['aap'] == "324")

    def test_handlers(self):
        self.assertEqual(len(self.webset.get_handlers()), 0)
        self.webset.addHandler("/suger/fly", "get", self.notrun)
        self.webset.addHandler("/", "get", self.notrun)
        self.assertEqual(len(self.webset.get_handlers()), 2)
        self.webset.remove_handler('/', 'post')
        self.assertEqual(len(self.webset.get_handlers()), 2)
        self.webset.remove_handler('/', 'get')
        self.assertEqual(len(self.webset.get_handlers()), 1)
        self.webset.remove_handler('/suger/fly')
        self.assertEqual(len(self.webset.get_handlers()), 0)

    def test_generate_headers(self):
        headerlist = self.webset._generate_headers({}, 200).split('\n')
        self.assertEqual(len(headerlist), 6)

    def test_splitpath(self):
        pathparams = {"POST": "/aap", "nooit": 123, "mies": 321}
        self.assertEqual(len(self.webset.splitpath(pathparams)), 4)

    def test_unquote(self):
        self.assertEqual(self.webset.unquote("abc%20def"), "abc def")

    def test_dictifyrequest(self):
        requestdata = "lol:   aap\nklont:   123\niets: 122,33\nversie: v1,2,alpha"
        dictsre = self.webset.dictifyrequest(requestdata)

        self.assertEqual(dictsre['LOL'], "aap")
        self.assertEqual(dictsre['KLONT'], 123)
        self.assertEqual(dictsre['IETS'], 122.33)
        self.assertEqual(dictsre['VERSIE'], "v1,2,alpha")


if __name__ == '__main__':
    unittest.main()
