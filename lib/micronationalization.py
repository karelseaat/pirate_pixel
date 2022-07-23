# ENABLEONBUILD 1
#import ujson as json

# DISABLEONBUILD 1
import json


class MicroNationalization:

    vars = []
    translatefile = ""
    pata = ""
    patb = ""

    def __init__(self, file, pata, patb):
        self.translatefile = open(file, "r+")
        self.pata = pata
        self.patb = patb

    def translate(self, text):
        self.getvars(text)
        return self.replacenames(text)

    def getvars(self, text):
        for value in text.split(self.pata)[1:]:
            bparts = value.split(self.patb)
            if bparts:
                self.vars.append(bparts[0].strip())

    def add_missing_to_file(self, adict, value):
        self.translatefile.seek(0, 0)
        adict.update({value: value})

        self.translatefile.write(json.dumps(adict))



    def replacenames(self, text):
        cont = self.translatefile.read()
        transdict = json.loads(cont)

        for value in self.vars:
            if value in transdict:
                text = text.replace(self.pata + " " + value + " " + self.patb, transdict[value])
            else:
                text = text.replace(self.pata + " " + value + " " + self.patb, value)
                self.add_missing_to_file(transdict, value)

        self.translatefile.seek(0, 0)
        return text
