#!/usr/bin/env python
import os
import sys

# REMOVEONBUILD 1
sys.dont_write_bytecode=True

# REMOVEONBUILD 1
import lib.network as network

from lib.microDNSSrv import MicroDNSSrv
from lib.validator import validator
from lib.websettings import websettings

from lib.connect import Connect
# from lib.hardware import hardware

from views import Views

# ok so if this server doesnt send enough data back to the client it will hang , ? dunno ?

klont = websettings()

conno = Connect(network.WLAN.STA_IF, backend_url="localhost", backend_port=5000)

# hw = hardware(conno)



view = Views(conno, klont)
# conno.set_config(view)
# conno.test_wifi()

conno.wifi_connect()

# conno.connect("blah", "blah")

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
klont.addHandler(r"\/makepost$", "get", view.makepost)
klont.addHandler(r"\/postpost$", "post", view.postit)



# ENABLEONBUILD 4
# domainsList = {"*": "127.0.0.1"}
# mdns = MicroDNSSrv()
# mdns.SetDomainsList(domainsList)
# mdns.Start()

if __name__ == "__main__":
    while True:
        # ENABLEONBUILD 1
        # mdns._serverProcess()
        klont._handle_client()
        conno.update()
        # hw.update()
