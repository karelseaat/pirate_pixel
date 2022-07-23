import unittest, os

if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.filehelper import filehelper
else:
    from lib.filehelper import filehelper


class TestAltFileHelper(unittest.TestCase):

    def test_read_writetext(self):
        pass
    #     filehelper("testfile.txt.nosave").open().replacetext("test text").writetext().close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "test text")
    #
    #     filehelper("testfile.txt.nosave").open().replacetext("kort").writetext().close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "kort")
    #
    #     filehelper("testfile.txt.nosave").open().replacetext("veel langer").writetext().close()
    #     self.assertTrue(filehelper("testfile.txt.nosave").open().readtext().close() == "veel langer")
    #     filehelper("testfile.txt.nosave").removefile()
    #
    # def test_read_writedict(self):
    #     fh = filehelper("testfile.json.nosave").open()
    #     fh.updatedict({'aap': 3, 'noot': 2, 'mies': [1, 2, 3]}).writedict().close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 3, 'noot': 2, 'mies': [1, 2, 3]})
    #
    #     fh.open().updatedict({'aap': 323234, 'noot': 2352352, 'mies': [1235235, 342, 376989]}).writedict().close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 323234, 'noot': 2352352, 'mies': [1235235, 342, 376989]})
    #
    #     fh.open().updatedict({'aap': 3, 'noot': 2, 'mies': [1, 2, 3]}).writedict().close()
    #     self.assertTrue(fh.open().readdict().close() == {'aap': 3, 'noot': 2, 'mies': [1, 2, 3]})
    #     fh.removefile()
    #
    # def test_read_writebin(self):
    #     filehelper("lolzor.bin.nosave").open(binary=True).replacebin(b"lsdfosdfo").writebinary().close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave", ).open(binary=True).readbinary().close() == b"lsdfosdfo")
    #
    #     filehelper("lolzor.bin.nosave").open(binary=True).replacebin(b"kort").writebinary().close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave").open(binary=True).readbinary().close() == b"kort")
    #
    #     filehelper("lolzor.bin.nosave").open(binary=True).replacebin(b"veel langer").writebinary().close()
    #     self.assertTrue(filehelper("lolzor.bin.nosave").open(binary=True).readbinary().close() == b"veel langer")
    #
    #     filehelper("lolzor.bin.nosave").removefile()
    #
    # def test_removefile(self):
    #     filehelper("todelete.txt.nosave").open().replacebin("test text").writebinary().close()
    #
    #     fh = filehelper("todelete.txt.nosave")
    #     self.assertTrue(fh.fileexists())
    #     fh.removefile()
    #     self.assertFalse(fh.fileexists())
    #
    # def test_make_not_fill(self):
    #     path = '/'.join(os.path.realpath(__file__).split('/')[:-2]) + "/"
    #     fh = filehelper("alttestfile.json.nosave", path=path).open().readdict()
    #     fh.updatedict({'aa':111, 'bbb': 333})
    #     self.assertTrue(fh.content == {'aa':111, 'bbb': 333})
    #     fh.updatedict({'qq':111, 'zzz': 333})
    #     self.assertTrue(fh.content == {'aa':111, 'bbb': 333, 'qq':111, 'zzz':333})
    #     fh.close()
    #
    # def test_update_file(self):
    #     path = '/'.join(os.path.realpath(__file__).split('/')[:-2]) + "/"
    #     fh = filehelper("alttestfile.json.nosave", path=path).open().readdict()
    #     fh.updatedict({'aa':111, 'bbb': 333})
    #     self.assertTrue(fh.content == {'aa':111, 'bbb': 333})
    #     fh.writedict()
    #     fh.readdict()
    #     self.assertTrue(fh.content == {'aa':111, 'bbb': 333})
    #     fh.close()
    #
    #
    # def test_removefile(self):
    #     path = '/'.join(os.path.realpath(__file__).split('/')[:-2]) + "/"
    #     fh = filehelper("alttestfile.json.nosave", path=path)
    #
    #     fh.removefile()
