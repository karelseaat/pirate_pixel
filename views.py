from lib.filehelper import filehelper
from lib.microWebTemplate import MicroWebTemplate
from lib.validator import validator
# from lib.micronationalization import MicroNationalization
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


        self.tempconfig = filehelper("./config.json").open().readdict()
        self.connection.set_config(self)


    def splitparams(self, params):
        return self.websettings.urlparse(params["GET"].split(" ")[0])[1]

    def limit_story(self, thelist):

        for item in thelist:
            if item['story']:
                item['story'] = item['story'][:30]

        return thelist

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

            'pagetitle': 'Pirate Pixy',
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

    def listsposts(self, requestparams):
        self.runeverytime(requestparams)
        tmpl = filehelper("./templates/faq.html").open().readtext().close()


        self.templatevars.update({"lol": self.tempconfig.content['POSTS']})
        self.templatevars.update({
            'pagetitle': 'Main'
        })

        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def showpost(self, requestparams):
        self.runeverytime(requestparams)
        idtoshow = int(requestparams['GET'].split(' ')[0].split('/')[-1])

        tmpl = filehelper("./templates/onepost.html").open().readtext().close()

        self.templatevars.update({"lol": self.tempconfig.content['POSTS'][idtoshow]})
        return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def makepost(self, requestparams):
                self.runeverytime(requestparams)
                tmpl = filehelper("./templates/apidocpost.html").open().readtext().close()
                self.templatevars.update({
                    'pagetitle': 'Main'
                })
                return {}, self.mWebTmpl.Execute(tmpl, self.templatevars), 200

    def postit(self, requestparams):

        vali = validator()
        vali.handleform(requestparams['POSTVALS'])

        if vali.error_free():
            self.tempconfig.addtodictlist(vali.get_values(), "POSTS")

        return  {'Location': '/listposts'}, '', 303
