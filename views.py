from lib.filehelper import filehelper
from lib.microWebTemplate import MicroWebTemplate
from lib.validator import validator
from lib.micronationalization import MicroNationalization
import time

dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

static_info = {'name': 'enterthematrix', 'soft_version': '0.1', 'hard_version': '0.1'}

class Views:
    connection = None
    websettings = None
    imediateredirect = None
    nationalisation = None
    tempconfig = None

    def __init__(self, connection, websettings):
        self.connection = connection
        self.connection.set_version(static_info)
        self.websettings = websettings
        self.templatevars = {}
        self.mWebTmpl = MicroWebTemplate()
        self.mWebTmpl.SetInternationaliser(MicroNationalization("nederlands.json", "[[", "]]"))

        self.tempconfig = filehelper("./config.json").open().readdict()
        if self.tempconfig.content['TESTAPS']:
            self.update_ap_statusus()

        self.connection.set_config(self)
        # self.connection.connect_avalable()

    def update_ap_statusus(self):
        allinrange = self.connection.get_accespoints()
        if 'APS' in self.tempconfig.content:
            for x in self.tempconfig.content['APS']:
                if x['WIFISSID'] in allinrange.keys():
                    self.connection.connect(x['WIFISSID'], x['WIFIPASSWD'])
                    time.sleep(0.5)
                    if self.connection.isconnected():
                        x['TESTCONNECT'] = 2
                    else:
                        x['TESTCONNECT'] = 1

        self.tempconfig.updatedict({'TESTAPS': False})
        self.tempconfig.writedict().close()
        quit()

    def splitparams(self, params):
        return self.websettings.urlparse(params["GET"].split(" ")[0])[1]

    def runeverytime(self, requestparams):
        self.templatevars = {}
        session = self.websettings.get_session_params()

        if session:
            self.templatevars.update(session)


        if 'GET' in requestparams:
            self.websettings.update_session_params({
                'prefurl': requestparams['GET'].split(' ')[0],
            })

        self.templatevars.update({
            'breadcrumbs': {
                'Unknown': '/',
            },
            'pagetitle': 'Unknown',
            'backendloggedin': self.connection.backend_loggedin()
        })


        if 'redirect' in self.templatevars:
            self.imediateredirect = self.templatevars['redirect']
        elif not self.websettings.isauthenticated():
            self.imediateredirect = {'Location': '/loginpage'}, '', 303
        else:
            self.imediateredirect = None


        self.templatevars.update({'dirty': self.tempconfig.is_dirty()})


        self.templatevars.update({
            'authenticated': self.websettings.isauthenticated(),
            'newsoftware': self.connection.get_version()[1],
            'newhardware': self.connection.get_version()[0],
            'connectionstatus': self.connection.getmodes(),
            'connected_to': self.connection.get_connected_to(),
            'connectionconfigs': {},
            'configset': {

            }
        })


        self.templatevars['CONNS'] = self.tempconfig.content['CONNS']


    def fourzerofour(self, requestparams):
        self.runeverytime(requestparams)

        tmpl = filehelper("./templates/fourzerofour.html").open().readtext().close()

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 404

    def mainpage(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/mainpage.html").open().readtext().close()

        self.templatevars.update({
            'breadcrumbs': {'Main': '/'},
            'pagetitle': 'Main'
        })

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def faq(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/faq.html").open().readtext().close()

        self.templatevars.update({
            'breadcrumbs': {'Main': '/'},
            'pagetitle': 'Main'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def connect(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/connect.html").open().readtext().close()


        self.templatevars.update({'connectionconfigs': self.tempconfig.content['CONNS']})

        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Connect': '/'},
            'pagetitle': 'Connect'
        })

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def configpage(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Config': '/config'},
            'pagetitle': 'Main Config'
        })

        tmpl = filehelper("./templates/config.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def getcss(self, requestparams):
        filename = self.splitparams(requestparams)[-1]
        tmpcss = filehelper("./static/css/" + filename).open().readtext().close()
        return {'Content-Type': 'text/css'}, tmpcss, 200

    def getimage(self, requestparams):
        filename = self.splitparams(requestparams)[-1]
        tmpimage = filehelper("./static/images/icons/" + filename).open().readtext().close()
        return {"Content-Type": "image/svg+xml"}, tmpimage, 200

    def getfavicon(self, requestparams):
        tmpimage = filehelper("./static/images/favicon.png").open(binary=True).readbinary().close()
        return {"Content-Type": "image/png"}, tmpimage, 200

    def getflag(self, requestparams):
        filename = self.splitparams(requestparams)[-1]

        tmpimage = filehelper("./static/images/flags/" + filename).open(binary=True).readbinary().close()

        return {"Content-Type": "image/png"}, tmpimage, 200

    def getgzipjs(self, requestparams):
        filename = self.splitparams(requestparams)[-1]
        filename = filename + ".gz"
        tmpjs = filehelper("./static/js/" + filename, binary=True).open().readbinary().close()
        return {"Content-Type": "text/javascript", "Content-Encoding": "gzip"}, tmpjs, 200

    def getjs(self, requestparams):
        filename = self.splitparams(requestparams)[-1]
        tmpjs = filehelper("./static/js/" + filename).open().readtext().close()
        return {"Content-Type": "text/javascript"}, tmpjs, 200

    def apconnectpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        apname = self.splitparams(requestparams)[-1]
        self.templatevars.update({'apname':apname})

        tmpl = filehelper("./templates/apconnect.html").open().readtext().close()

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def aptestpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect


        tmpl = filehelper("./templates/aptest.html").open().readtext().close()

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def apsetpage(self, requestparams):
        self.runeverytime(requestparams)

        paramp = self.splitparams(requestparams)
        self.templatevars.update({'selected':'none'})
        if 'APS' in self.tempconfig.content:
            for ap in self.tempconfig.content['APS']:
                if ap['WIFISSID'] == paramp[-1]:
                    self.templatevars.update({'selected':ap['WIFISSID']})

        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Config': '/config',
                'Ap Config': '/apset'
            },
            'pagetitle': 'AP Config'
        })

        if 'postresults' in requestparams:
            self.templatevars.update({
                'postresults': requestparams['postresults']
            })
            self.templatevars.update({
                'snackmesg': 'contains errors',
                'snackclass': 'msgred'
            })
            # {**{'ConnectAThing':'off', 'AdaFruit':'off', 'API':'off', 'CustomMqtt':'off'}, **requestparams['POSTVALS']}

        accpoints = {**{'--None--':''}, **self.connection.get_accespoints()}
        self.templatevars.update({'accesspoints': accpoints})

        tmpl = filehelper("./templates/apset.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def apconfigpage(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Config': '/config',
                'ApConfig': '/apconfig'
            },
            'pagetitle': 'AP Config'
        })

        tmpl = filehelper("./templates/apconfig.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def veriviedappage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        allinrange = self.connection.get_accespoints()

        if 'APS' in self.tempconfig.content:
            # beetje smerig
            temp = []
            for x in self.tempconfig.content['APS']:
                temp.append({**x,**{'allready':x['WIFISSID'] in allinrange.keys() and x['TESTCONNECT'] == 2, 'inrange': x['WIFISSID'] in allinrange.keys(),'oddeven':self.tempconfig.content['APS'].index(x) % 2}})
                # x.update({'allready':x['WIFISSID'] in allinrange.keys() and x['TESTCONNECT'] == 2, 'inrange': x['WIFISSID'] in allinrange.keys(),'oddeven':self.tempconfig.content['APS'].index(x) % 2})

            self.templatevars.update({'accesspoints': temp})

        tmpl = filehelper("./templates/apreport.html").open().readtext().close()
        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Config': '/config',
                'ConnectConfig': '/connectconfig'
            },
            'pagetitle': 'Connect Config'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def removeveriviedap(self, requestparams):
        aptoremove = self.splitparams(requestparams)[-1]

        newAPS = []
        if 'APS' in self.tempconfig.content:
            for x in self.tempconfig.content['APS']:
                if x['WIFISSID'] != aptoremove:
                    # print(x, "----------------------------")
                    # x = dictfilt(x, ['WIFISSID', 'WIFIPASSWD'])
                    newAPS.append(x)
            self.tempconfig.updatedict({"APS": newAPS}).writedict()
            self.websettings.update_session_params({
                'snackmesg': 'Removed AP',
                'snackclass': 'msggreen'
            })

        return {'Location': '/config/apconfig'}, '', 303

    def appostpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect



        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if vali.error_free():

            # hier moet een redirect komen naar een pagina die uitlegt dat het device aan het herstarten is en dat je na een minuut mag reconnecten om te kijken of de
            # connection gelukt is waarna je je accesspoint mag uitzoeken uit de lijst met mogelijke accespoints in de accespointreport
            allofit = {**vali.get_values(), **{'TESTCONNECT': 0, 'USETHIS': False}}
            added = False
            for ap in self.tempconfig.content['APS']:
                if ap['WIFISSID'] == allofit['WIFISSID']:
                    ap = allofit
                    added = True
                    break

            if not added:
                self.tempconfig.content['APS'].append(allofit)

            self.tempconfig.writedict()

            self.websettings.update_session_params({
                'snackmesg': 'OK !!!!',
                'snackclass': 'msggreen'
            })

            return  {'Location': '/config/apconfig'}, '', 303
        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return {'Location': '/config/apset'}, '', 303


    def loginconfigpage(self, requestparams):
        self.runeverytime(requestparams)

        lolzor = "Nope"

        if self.imediateredirect:
            return self.imediateredirect

        if 'login' in self.tempconfig.content:
            lolzor = self.tempconfig.content['login']

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Config': '/config',
                'LoginConfig': '/loginconfig'
            },
            'pagetitle': 'Password Config',
            'login': lolzor
        })

        tmpl = filehelper("./templates/loginconfig.html").open().readtext().close()
        if 'postresults' in requestparams:
            self.templatevars.update({'postresults': requestparams['postresults']})
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def loginconfigpostpage(self, requestparams):

        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        import hashlib
        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if vali.error_free():

            m = hashlib.sha256()
            m.update(str.encode(vali.get_values()['ADMINPASSWD']))
            self.tempconfig.updatedict({'ADMINPASSWD': m.hexdigest()})
            self.websettings.update_session_params({
                'snackmesg': 'OK !!!!',
                'snackclass': 'msggreen'
            })
            return  {'Location': '/config'}, '', 303
        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return  {'Location': '/loginconfig'}, '', 303

    def connectconfigpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/connectconfig.html").open().readtext().close()

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Config': '/config',
                'ConnectConfig': '/connectconfig'
            },
            'pagetitle': 'Connect Config'
        })

        if 'CONNS' in self.tempconfig.content:
            klontzer = self.tempconfig.content['CONNS']

        externalconns = ['ConnectAThing', 'AdaFruit', 'API', 'CustomMqtt']
        beter = {}
        for v in externalconns:
            if v in klontzer and klontzer[v] == 'on':
                beter.update({v:'checked'})
            else:
                beter.update({v:''})


        self.templatevars.update({'externalconns': beter})
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def connectpostpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect
        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        externalconns = {**{'ConnectAThing':'off', 'AdaFruit':'off', 'API':'off', 'CustomMqtt':'off'}, **requestparams['POSTVALS']}


        if vali.error_free():
            self.tempconfig.updatedict({"CONNS": externalconns})


            return  {'Location': '/config'}, '', 303
        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
            })
            return  {'Location': '/connectconfig'}, '', 303


    def connecttestpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect
        return  {'Location': '/'}, '', 303

    def custommqtt(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/custommqtt.html").open().readtext().close()

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'custommqtt': '/custommqtt'
            },
            'pagetitle': 'Custom Mqtt'
        })

        if 'postresults' in requestparams:
            # self.templatevars.update({'postresults': requestparams['postresults']})
            self.templatevars.update({
                'postresults': requestparams['postresults'],
                'snackmesg': 'Errors in form.',
                'snackclass': 'msgred'
            })

        # if 'mqtt' in self.tempconfig.content:
        #     boff = self.tempconfig.content['mqtt']

        self.templatevars.update({'mqtt': self.tempconfig.content})
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def mqttpostpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if  vali.error_free():

            self.tempconfig.updatedict(vali.get_values())
            self.websettings.update_session_params({
                'snackmesg': 'Form is OK !!!',
                'snackclass': 'msggreen'
            })
            return  {'Location': '/connect'}, '', 303
        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return  {'Location': '/custommqtt'}, '', 303

    def adafruitmqtt(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect


        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'AdaFruit Config': '/adafruitmqtt'
            },
            'pagetitle': 'Adafruit Config'
        })

        self.templatevars.update(self.tempconfig.content)
        tmpl = filehelper("./templates/adafruit.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def adafruitmqttpostpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])


        if vali.error_free():
            self.tempconfig.updatedict(vali.get_values())

            self.websettings.update_session_params({
                'snackmesg': 'Data saved !',
                'snackclass': 'msggreen'
            })
            return {'Location': '/connect'}, '', 303
        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return {'Location': '/adafruitmqtt'}, '', 303

    def connectathing(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'custommqtt': '/connectathing'
            },
            'pagetitle': 'ConnectAThing'
        })

        tmpl = filehelper("./templates/connectathing.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def catregisteruserpost(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect
        import json

        postvals = requestparams['POSTVALS']

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if not vali.error_free():

            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return {'Location': '/connectathing'}, '', 303
        else:
            messages = ["An connection error.", "Didnt get a 200 code while connecting.", "we are not connected to  network so there is no change to connet to the backend !"]

            code = self.connection.register_user(json.dumps(postvals))

            code = self.websettings.numerfy(code)

            if not code.isdigit():
                self.websettings.update_session_params({
                    'snackmesg': code,
                    'snackclass': 'msggreen'
                })

            elif code in messages:
                self.websettings.update_session_params({
                    'snackmesg': messages[code],
                    'snackclass': 'msgred'
                })

            return {'Location': '/'}, '', 303




    def catregisteruser(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'custommqtt': '/connectathing',
                'Register User': '/catregisteruser'
            },
            'pagetitle': 'Register User'
        })

        tmpl = filehelper("./templates/catregisteruser.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def catlogin(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'custommqtt': '/connectathing',
                'Login': '/catlogin'
            },
            'pagetitle': 'Login User'
        })

        tmpl = filehelper("./templates/catlogin.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def registerdevice(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        code = self.connection.register_connect_a_thing()
        # code = self.websettings.numerfy(code)


        if not code.isdigit():
            self.websettings.update_session_params({
                'snackmesg': code,
                'snackclass': 'msggreen'
            })

        elif code in messages:
            self.websettings.update_session_params({
                'snackmesg': messages[code],
                'snackclass': 'msgred'
            })

        return {'Location': '/'}, '', 303

    def deregisterdevice(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        code = self.connection.deregister_connect_a_thing()

        if not code.isdigit():
            self.websettings.update_session_params({
                'snackmesg': code,
                'snackclass': 'msggreen'
            })

        elif code in messages:
            self.websettings.update_session_params({
                'snackmesg': messages[code],
                'snackclass': 'msgred'
            })

        return {'Location': '/'}, '', 303



    def catregderegdevice(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        self.templatevars.update({
            'breadcrumbs': {
                'Main': '/',
                'Connect': '/connect',
                'custommqtt': '/connectathing',
                'Login': '/catlogin'
            },
            'pagetitle': 'Register Device',
            'mac': self.connection.network_config('mac')
        })

        tmpl = filehelper("./templates/catregderegdevice.html").open().readtext().close()
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def catloginpost(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        import json
        postvals = requestparams['POSTVALS']

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if not vali.error_free():

            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return {'Location': '/connectathing'}, '', 303
        else:

            messages = ["An connection error.", "Didnt get a 200 code while connecting.", "we are not connected to  network so there is no change to connet to the backend !"]

            code = self.connection.login_user(json.dumps(postvals))


            code = self.websettings.numerfy(code)

            if not code.isdigit():
                self.websettings.update_session_params({
                    'snackmesg': code,
                    'snackclass': 'msggreen'
                })

            elif code in messages:
                self.websettings.update_session_params({
                    'snackmesg': messages[code],
                    'snackclass': 'msgred'
                })

            return {'Location': '/'}, '', 303

    # def connactathingpostpage(self, requestparams):
    #     self.runeverytime(requestparams)
    #
    #     if self.imediateredirect:
    #         return self.imediateredirect
    #
    #     import json
    #     postvals = requestparams['POSTVALS']
    #
    #     vali = validator()
    #     vali.handleform(requestparams['POSTVALS'])
    #
    #     if not vali.error_free():
    #
    #         self.websettings.update_session_params({
    #             "postresults": vali.get_results(),
    #             'snackmesg': 'Errors in form',
    #             'snackclass': 'msgred'
    #         })
    #         return {'Location': '/connectathing'}, '', 303
    #     else:
    #         postvals.update({'mac': self.connection.network_config('mac')})
    #
    #         messages = ["An connection error.", "Didnt get a 200 code while connecting.", "we are not connected to  network so there is no change to connet to the backend !"]
    #
    #         code = self.connection.register_connect_a_thing(json.dumps(postvals))
    #         code = self.websettings.numerfy(code)
    #
    #         if not code.isdigit():
    #             self.websettings.update_session_params({
    #                 'snackmesg': code,
    #                 'snackclass': 'msggreen'
    #             })
    #
    #         elif code in messages:
    #             self.websettings.update_session_params({
    #                 'snackmesg': messages[code],
    #                 'snackclass': 'msgred'
    #             })
    #
    #         return {'Location': '/'}, '', 303

    def apipost(self, requestparams):
        mydict = {'status': 'ok'}
        return {'Content-Type': 'application/json'}, mydict, 200

    def apiget(self, requestparams):
        buttons = {'knop1': 1000, 'knop2': 500, 'knop3': 1200}
        return {'Content-Type': 'application/json'}, buttons, 200

    def apidocget(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/apidocget.html").open().readtext().close()
        self.templatevars.update({'ipaddress': self.connection.ip_config()[0], 'port': self.websettings.getport()})
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Connect':'/connect', 'Api': '/apidoc','Get Buttons':'/apidocget'},
            'pagetitle': 'Get Buttons'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def apibuttonsget(self, requestparams):
        import base64

        base64_bytes = base64.b64decode(requestparams['AUTHORIZATION'].split(' ')[1])

        if base64_bytes.decode('ascii').split(':')[1] == self.tempconfig.content['APIAUTHASSWORD']:
            return {}, 'all good', 200
        else:
            return {}, 'bad auth', 200

    def apidocpost(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        if 'postresults' in requestparams:
            self.templatevars.update({'postresults': requestparams['postresults']})

        tmpl = filehelper("./templates/apidocpost.html").open().readtext().close()
        self.templatevars.update({'ipaddress': self.connection.ip_config()[0], 'port': self.websettings.getport()})
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Connect':'/connect', 'Api': '/apidoc','Post To Matrix':'/apidocpost'},
            'pagetitle': 'Post To Matrix'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def apiscreenpost(self, requestparams):
        import base64


        if 'AUTHORIZATION' not in requestparams:
            # nog foutmelding toevoegen in de snackbar !
            return {}, 'authentication did not work out !', 200

        base64_bytes = base64.b64decode(requestparams['AUTHORIZATION'].split(' ')[1])

        if base64_bytes.decode('ascii').split(':')[1] == self.tempconfig.content['APIAUTHASSWORD']:
            return {}, 'all good', 200

        return {}, 'bad auth', 200

    def loginpage(self, requestparams):
        self.runeverytime(requestparams)

        self.websettings.setsession()

        tmpl = filehelper("./templates/login.html").open().readtext().close()

        self.templatevars.update({
            'breadcrumbs': {
                'Login': '/loginpage',
            },
            'pagetitle': 'Login'
        })

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def loginpostpage(self, requestparams):
        self.runeverytime(requestparams)
        import hashlib
        m = hashlib.sha256()
        m.update(str.encode(requestparams['POSTVALS']['password']))



        if 'ADMINPASSWD' in self.tempconfig.content and self.tempconfig.content['ADMINPASSWD'] == m.hexdigest():
            self.websettings.authenticate()
            return {'Location': '/'}, '', 303
        else:
            self.websettings.update_session_params({
                'snackmesg': 'Password was not corrent !',
                'snackclass': 'msgred'
            })
            return {'Location': '/loginpage'}, '', 303

    def logoutpage(self, requestparams):
        self.websettings.deauthenticate()
        return {'Location': '/'}, '', 303

    def apipage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/apidoc.html").open().readtext().close()
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Connect':'/connect' ,'Api': '/apidoc'},
            'pagetitle': 'Apidoc'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200


    def apiauth(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/apiauth.html").open().readtext().close()
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Connect':'/connect' ,'Api': '/apidoc', 'ApiAuth': '/apiauth'},
            'pagetitle': 'Api Auth'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def apiauthpostpage(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if vali.error_free():

            self.tempconfig.updatedict(vali.get_values())
            self.websettings.update_session_params({
                'snackmesg': 'Data saved !',
                'snackclass': 'msggreen'
            })
            return {'Location': '/apidoc'}, '', 303

        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })
            return {'Location': '/apiauth'}, '', 303

    def helpmain(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        tmpl = filehelper("./templates/helpmain.html").open().readtext().close()
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Help':'/helpmain' },
            'pagetitle': 'Help'
        })
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def customersup(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect



        tmpl = filehelper("./templates/customersup.html").open().readtext().close()
        self.templatevars.update({
            'breadcrumbs': {'Main': '/', 'Customer suport':'/customersup' },
            'pagetitle': 'Customer suport'
        })

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def customersuppost(self, requestparams):
        self.runeverytime(requestparams)
        if self.imediateredirect:
            return self.imediateredirect

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])
        if vali.error_free():

            # hier moet een redirect komen naar een pagina die uitlegt dat het device aan het herstarten is en dat je na een minuut mag reconnecten om te kijken of de
            # connection gelukt is waarna je je accesspoint mag uitzoeken uit de lijst met mogelijke accespoints in de accespointreport
            allofit = vali.get_values()
            if 'chatid' in allofit:
                chatid = allofit['chatid']
            else:
                chatid = 0
            message = self.connection.send_customer_message(allofit['question'], chatid).replace('\n', '')[1:-1].split(',')

            # print('blaats $%^', type(message), message)
            # if not is_integer(message[0]):
            #     message[0] = self.websettings.numerfy(message[0])
            #
            # print("test")

            # if not question.isdigit():

            self.websettings.update_session_params({
                'snackmesg': 'Message send !',
                'snackclass': 'msggreen',
                'chatcontent': message[0],
                'chatid': self.websettings.numerfy(message[1])
            })
            # else:
            #     self.websettings.update_session_params({
            #         'snackmesg': 'Server reacted in a strange way !',
            #         'snackclass': 'msgred'
            #     })

        else:
            self.websettings.update_session_params({
                "postresults": vali.get_results(),
                'snackmesg': 'Errors in form',
                'snackclass': 'msgred'
            })

        return {'Location': self.templatevars['prefurl']}, '', 303


    def resetdevicetest(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        # here do device reset !
        self.tempconfig.updatedict({"TESTAPS": True})
        self.tempconfig.writedict().close()
        quit()

        return {}, 'normaly you should not be able to reach this page, since device reset', 200


    def resetdeviceconnect(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        apname = self.splitparams(requestparams)[-1]

        newAPS = []
        if 'APS' in self.tempconfig.content:
            for x in self.tempconfig.content['APS']:
                x = dictfilt(x, ['WIFISSID', 'WIFIPASSWD', 'TESTCONNECT', 'USETHIS'])
                if x['WIFISSID'] == apname:
                    x['USETHIS'] = True
                newAPS.append(x)
        self.tempconfig.updatedict({"APS": newAPS})
        self.tempconfig.writedict().close()
        quit()

        return {}, 'normaly you should not be able to reach this page, since device reset', 200

    def saveconfig(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        self.tempconfig.writedict().close()

        return {'Location': self.templatevars['prefurl']}, '', 303

    def languagechoose(self, requestparams):
        self.runeverytime(requestparams)

        if self.imediateredirect:
            return self.imediateredirect

        langs = {'de':'duits.json', 'nl':'nederlands.json', 'en':'engels.json'}
        langname = self.splitparams(requestparams)[-1]

        if langname in langs:
            self.mWebTmpl.SetInternationaliser(MicroNationalization(langs[langname], "[[", "]]"))

        return {'Location': self.templatevars['prefurl']}, '', 303
