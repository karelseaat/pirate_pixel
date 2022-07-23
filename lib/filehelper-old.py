# ENABLEONBUILD 2
#import ujson as json
#import uos as os

# DISABLEONBUILD 3
import json
import os
import time


class filehelper(object):
    """
    this class will help open and write files for text, binary and config/json
    """

    afile = None
    filename = ""
    content = ""

    def __init__(self, filename=None, binary=False):
        self.binary = binary
        if not filename:
            self.filename = None
            return
        if filename[0:1] != "./":
            filename = "./" + filename
        self.filename = filename

    def getticks(self):
        """
        this function should not be here but lack of a better place.
        this could be used to measure the timing

        Params: None
        Return: the time in mili seconds ?
        """
        return time.clock()


    def getpath(self):
        """
        Of the file path of the file get file dir part

        Params: The filename with  the path.
        Return: The path part of the filename and path.
        """
        alist = self.filename.split("/")
        return "/".join(alist[:-1])

    def getfile(self):
        """
        Of the file path of the file get file name part.

        Params: The filename wih the path.
        Return: The file name of the filename and path.

        """
        return self.filename.split("/")[-1]

    def removefile(self):
        """
        Remove the file.

        Params: None
        Return: None

        """
        os.remove(self.filename)

    def fileexists(self):
        """
        Test if the file realy exists

        Params: None
        Return: True or False (file exists or not)
        """
        if not self.filename:
            return False
        filepath = self.getpath()
        return self.getfile() in os.listdir(filepath)

    def open(self):
        """
        open the file in normal or binary mode and create it if it doesnt exist, depends on opening mode.

        Params: binary mode  True or False
        Return: None
        """
        if not self.fileexists():
            if self.binary:
                self.afile = open(self.filename, 'wb+')
            else:
                self.afile = open(self.filename, 'w+')
        else:
            if self.binary:
                self.afile = open(self.filename, 'rb+')
            else:
                self.afile = open(self.filename, 'r+')

        return self

    def close(self):
        """
        close the file and return the content !

        Params: None
        Return: the file content
        """
        self.afile.close()
        content = self.content
        self.content = ""
        return content

    def readtext(self):
        """
        read the text from a file and return the content

        Params: None
        Return: content of the file in normal text
        """
        try:
            self.content = self.afile.read()
        except Exception as e:
            print(e)
            self.content ="File not found !"

        return self

    def writebinary(self, bin):
        """
        write to the file as being a binary file

        Params: Binary data
        Return: None
        """
        self.afile.truncate(0)
        self.afile.write(bin)
        return self

    def readbinary(self):
        """
        read the file as being a binary file

        Params: None
        Return: A binary data string
        """
        try:
            self.content = self.afile.read()
        except Exception as e:
            print(e)
            self.content = "File not found !"
        return self

    def writetext(self, text):
        """
        write a file as text

        Params: The text to write to the file
        Return: None
        """
        self.afile.truncate(0)
        self.afile.write(text)
        return self


    def writedict(self, adict):
        """
        write a file as a dict = json

        Params: the dictionary you want to write
        Return: None
        """
        self.afile.truncate(0)
        self.afile.seek(0)
        self.afile.write(json.dumps(adict))
        return self

    def addtodictlist(self, item, key):
        """
            add a item to a list in a dict for use in json save

            Params: item to add to the list , key the key we want to add this in the content dict
            return: self
        """
        self.readdict(forupdate=True)
        if key in self.content:
            self.content[key].append(item)

        self.writedict(self.content)
        return self

    def remfromdictlist(self, key, index):
        """
            remove a item from a list in a dict for use in json save

            Params: index of the item to remove from the list, key the key we want to add this in the content dict
            return: self
        """
        self.readdict(forupdate=True)
        if key in self.content and len(self.content[key]) <= index:
            del self.content[key][index]
        self.writedict(self.content)
        return self


    def updatedict(self, adict):
        """
        Rewrite a dict file with new dict items.

        Params: The dictionary you want to append.
        Return: None
        """
        self.readdict(forupdate=True)

        self.content.update(adict)
        self.writedict(self.content)

        return self


    def readdict(self, vals_expected=[], forupdate=False):
        """
        read a file as a dictionary/ujson

        Params: vals_expected , can be removed ? forupdate ???
        Return: A dictionary with the content
        """

        if forupdate:
            self.afile.seek(0)
        try:
            content = self.afile.read()
            self.content = json.loads(content.strip())
        except Exception as e:
            print(e)
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno)
            self.content = {}
        return self
