import unittest, os


if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.filehelper import filehelper
else:
    from lib.filehelper import filehelper


class TestFileHelper(unittest.TestCase):

    def test_read_writetext(self):
        pass
    #     filehelper("testfile.txt.nosave").open().writetext("test text").close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "test text")
    #
    #     filehelper("testfile.txt.nosave").open().writetext("kort").close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "kort")
    #
    #     filehelper("testfile.txt.nosave").open().writetext("veel langer").close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "veel langer")
    #     filehelper("testfile.txt.nosave").removefile()
    #
    # def test_read_writedict(self):
    #     fh = filehelper("testfile.json.nosave").open()
    #     fh.writedict({'aap': 3, 'noot': 2, 'mies': [1, 2, 3]}).close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 3, 'noot': 2, 'mies': [1, 2, 3]})
    #
    #
    #     fh.open().writedict({'aap': 323234, 'noot': 2352352, 'mies': [1235235, 342, 376989]}).close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 323234, 'noot': 2352352, 'mies': [1235235, 342, 376989]})
    #
    #     fh.open().writedict({'aap': 3, 'noot': 2, 'mies': [1, 2, 3]}).close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 3, 'noot': 2, 'mies': [1, 2, 3]})
    #     fh.removefile()
    #
    # def test_read_writebin(self):
    #     filehelper("lolzor.bin.nosave", binary=True).open().writebinary(b"lsdfosdfo").close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave", binary=True).open().readbinary().close() == b"lsdfosdfo")
    #
    #     filehelper("lolzor.bin.nosave", binary=True).open().writebinary(b"kort").close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave", binary=True).open().readbinary().close() == b"kort")
    #
    #     filehelper("lolzor.bin.nosave", binary=True).open().writebinary(b"veel langer").close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave", binary=True).open().readbinary().close() == b"veel langer")
    #
    #     filehelper("lolzor.bin.nosave", binary=True).removefile()
    #
    # def test_removefile(self):
    #     filehelper("todelete.txt.nosave").open().writetext("test text").close()
    #
    #     fh = filehelper("todelete.txt.nosave")
    #     self.assertTrue(fh.fileexists())
    #     fh.removefile()
    #     self.assertFalse(fh.fileexists())
