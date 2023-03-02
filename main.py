#!/usr/bin/env python
import os
import sys

sys.dont_write_bytecode=True

import lib.network as network

from lib.microDNSSrv import MicroDNSSrv
from lib.validator import validator
from lib.websettings import websettings

from lib.connect import Connect

from views import Views



klont = websettings()

conno = Connect(network.WLAN.STA_IF, backend_url="localhost", backend_port=5000)


view = Views(conno, klont)

conno.wifi_connect()



klont.set_fourzerofour(view.fourzerofour)

# get assets

klont.addHandler(r"\/getcss\/.*\.css$", "get", view.getcss)
klont.addHandler(r"\/getimage\/.*\.svg$", "get", view.getimage)
klont.addHandler(r"\/getflag\/.*\.png$", "get", view.getflag)
klont.addHandler(r"\/favicon\.ico$", "get", view.getfavicon)
klont.addHandler(r"\/getgzipjs\/.*\.js$", "get", view.getgzipjs)
klont.addHandler(r"\/getjs\/.*\.js$", "get", view.getjs)

# pirate pages

klont.addHandler(r"\/listposts$", "get", view.listsposts)
klont.addHandler(r"\/showpost\/.*$", "get", view.showpost)
klont.addHandler(r"\/makepost$", "get", view.makepost)
klont.addHandler(r"\/postpost$", "post", view.postit)



if __name__ == "__main__":
    while True:
        klont._handle_client()
        conno.update()
