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
from lib.hardware import hardware

from views import Views

# ok so if this server doesnt send enough data back to the client it will hang , ? dunno ?

klont = websettings()

conno = Connect(network.WLAN.STA_IF, backend_url="localhost", backend_port=5000)

hw = hardware(conno)



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

# config

klont.addHandler(r"\/config$", "get", view.configpage)
klont.addHandler(r"\/config\/apconfig$", "get", view.apconfigpage)
klont.addHandler(r"\/config\/aptest$", "get", view.aptestpage)

klont.addHandler(r"\/config\/loginconfig", "get", view.loginconfigpage)
klont.addHandler(r"\/config\/loginconfig$", "post", view.loginconfigpostpage)
klont.addHandler(r"\/config\/connectconfig", "get", view.connectconfigpage)
klont.addHandler(r"\/config\/connectconfig", "post", view.connectpostpage)
klont.addHandler(r"\/config\/connecttest$", "get", view.connecttestpage)

# config/apconfig

klont.addHandler(r"\/config\/apset(\/?.*)$", "get", view.apsetpage) # zo aanpassen dat het ook werkt voor edit !
klont.addHandler(r"\/config\/apset$", "post", view.appostpage)
klont.addHandler(r"\/config\/veriviedap$", "get", view.veriviedappage)
klont.addHandler(r"\/config\/removeveriviedap\/.*$", "get", view.removeveriviedap)
klont.addHandler(r"\/config\/apconnect\/.*$", "get", view.apconnectpage)

# connect

klont.addHandler(r"\/connect$", "get", view.connect)
klont.addHandler(r"\/connect\/adafruitmqtt$", "get", view.adafruitmqtt)
klont.addHandler(r"\/connect\/adafruitmqtt$", "post", view.adafruitmqttpostpage)
klont.addHandler(r"\/connect\/custommqtt$", "get", view.custommqtt)
klont.addHandler(r"\/connect\/custommqtt$", "post", view.mqttpostpage)

# connect/api

klont.addHandler(r"\/connect\/apidocget$", "get", view.apidocget)
klont.addHandler(r"\/connect\/apidoc$", "get", view.apipage)
klont.addHandler(r"\/connect\/apibuttonsget$", "get", view.apibuttonsget)
klont.addHandler(r"\/connect\/apidocpost$", "get", view.apidocpost)
klont.addHandler(r"\/connect\/apiauth$", "get", view.apiauth)
klont.addHandler(r"\/connect\/apiauth$", "post", view.apiauthpostpage)
klont.addHandler(r"\/connect\/api$", "get", view.apiget)
klont.addHandler(r"\/connect\/api$", "post", view.apipost)
klont.addHandler(r"\/connect\/apiscreenpost$", "post", view.apiscreenpost)

# connect/connectathing

klont.addHandler(r"\/connect\/connectathing$", "get", view.connectathing)
klont.addHandler(r"\/connect\/catregisteruser$", "get", view.catregisteruser)
klont.addHandler(r"\/connect\/catregisteruser$", "post", view.catregisteruserpost)
klont.addHandler(r"\/connect\/catlogin$", "get", view.catlogin)
klont.addHandler(r"\/connect\/catlogin$", "post", view.catloginpost)
klont.addHandler(r"\/connect\/catregderegdevice$", "get", view.catregderegdevice)
klont.addHandler(r"\/connect\/registerdevice$", "get", view.registerdevice)
klont.addHandler(r"\/connect\/deregisterdevice$", "get", view.deregisterdevice)


# authentication

klont.addHandler(r"\/loginpage$", "get", view.loginpage)
klont.addHandler(r"\/loginpage$", "post", view.loginpostpage)
klont.addHandler(r"\/logoutpage", "get", view.logoutpage)

#help

klont.addHandler(r"\/helpmain$", "get", view.helpmain)
klont.addHandler(r"\/customersup$", "get", view.customersup)
klont.addHandler(r"\/customersup$", "post", view.customersuppost)
klont.addHandler(r"\/faq$", "get", view.faq)

# assorted

klont.addHandler(r"/$", "get", view.mainpage)

klont.addHandler(r"\/resetdevicetest$", "get", view.resetdevicetest)
klont.addHandler(r"\/resetdeviceconnect\/.*$", "get", view.resetdeviceconnect)
klont.addHandler(r"\/saveconfig$", "get", view.saveconfig)
klont.addHandler(r"\/languagechoose\/.*$", "get", view.languagechoose)

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
        hw.update()
