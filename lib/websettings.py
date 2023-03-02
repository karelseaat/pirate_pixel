#!/usr/bin/python3
import sys
import time
from os import urandom as rnd

import re
import json
import socket
import sys
import os
import binascii as ubinascii


class websettings:
    """
    This class will do alot of the webserving and the framework like
    functionality.
    Perhaps the frmework and the webserving functionality should be split ?

    """

    def __init__(self,port=8080):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.s.bind(('', port))
        self.s.listen(1)
        self.s.setblocking(False)
        self.s.settimeout(0.5)
        self.handlers = {}
        self._hextobyte = None
        self._hexdig = '0123456789ABCDEFabcdef'
        self.authenticated = ''

        self.session = None
        self.session_container = {}

    def getport(self):
        return self.port

    def isauthenticated(self):
        """
        This function will return a true is the user is authenticated
        and a false otherwize.

        Params: None

        Return: if the user is authenticated or not True, False
        """
        return (
            bool(self.authenticated)
            and
            bool(self.session)
            and
            self.session == self.authenticated
        )

    def authenticate(self):
        """
        This will put the current session to the authenticated session.

        Params: None
        Return: None
        """
        self.authenticated = self.session

    def get_session_params(self):
        if self.session in self.session_container:
            content = self.session_container[self.session]
            self.session_container = {self.session:{}}
            return content

    def set_session_params(self, params):
        if self.session in self.session_container:
            self.session_container[self.session] = params

    def update_session_params(self, params):
        if self.session in self.session_container:
            self.session_container[self.session].update(params)

    def deauthenticate(self):
        self.delsession()


    def randhex(self, num):
        """
        This will return a random hetidecimal number of num length.

        Params:num number of hex numbers
        Return:the hex number
        """
        return ubinascii.hexlify(rnd(num)).decode("utf-8")

    def randnum(self, num):
        return int((ord(rnd(1))/256) * num)

    def __del__(self):
        self.s.close()

    def setsession(self):
        """
        Set the session to a randomhexnumber of 8

        Params: None
        Return: The name/number of the session
        """
        if not self.session:
            self.session = self.randhex(8)
            self.session_container = {self.session:{}}

    def delsession(self):
        """
        Destroy the current session, by setting the session to None

        Params: None
        Return: None
        """
        del self.session_container[self.session]
        self.session = None


    def urlparse(self, url):
        """
        Not a full url parse, perhaps in the futuremainly the url part
        and the parameters get plit here and returned.
        Perhaps later use something like this:
        https://github.com/lucien2k/wipy-urllib/blob/master/urllib.py

        Params: the url to be parsed

        Return: a neat dict of seperated url parameters
        """
        url = url.strip().split(' ', 1)[0]
        path = []
        params = []
        paradict = {}

        if "?" in url:
            path, params = url.split('?', 1)
            paradict = self.splitparams(params)
        else:
            path = url

        # path = path.split("/")
        # del path[1]
        return paradict, path.split("/")

    def splitparams(self, params):
        """
        An extra part that splits the parameters.
        Params: Params to be split based on = or &

        Return: A dict of key values based on the params
        """
        return dict(para.split("=") for para in params.split("&"))

    def clear_handlers(self):
        """
        Clear the handlers that handle web requests, so there are no more routes to take

        Params: None
        Return: None
        """
        self.handlers = {}

    def addHandler(self, pathname, method, handler):
        """
        Add a new handler for a webrequest.

        Params: pathname the path or url you would type in your browser, The method GET, POST, PATCH, and the handler method in the views to code handle you request
        Return: None
        """
        self.handlers.update({(pathname, method.upper()): handler})

    def list_handlers(self):
        """
        List and print all handlers.

        Params: None
        Return: None
        """
        for value in self.handlers:
            print(value, self.handlers[value])

    def get_handlers(self):
        """
        Return the handlers that you have.

        Params: None
        Return: The handlers in the form of a list of dicts
        """
        return self.handlers

    def remove_handler(self, handlername, handlertype=""):
        """
        remove a handler by handler name and handler type

        Params: the handler name , the handlertype = POST or  GET or PATCH etc
        return None
        """
        temp = {}
        if handlertype != "":
            if (handlername, handlertype.upper()) in self.handlers:
                for value in self.handlers:
                    if value != (handlername, handlertype.upper()):
                        temp.update({value: self.handlers[value]})
            else:
                return
        else:
            handlernames = [hn[0] for hn in self.handlers]
            if (handlername in handlernames):
                for value in self.handlers:
                    if value[0] != handlername:
                        temp.update({value: self.handlers[value]})
            else:
                return

        self.handlers = temp

    def _generate_headers(self, extra, response_code):
        """
        when generating a response this will create the header of a html
        reponse.
        This can use refactoring

        Params:
        Return: A HTML Header
        """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'
        elif response_code == 303:
            header += 'HTTP/1.1 303 See Other\n'

        if self.session:
            header += "Set-Cookie: session={}\n".format(self.session)

        for key in extra:
            header += key + ": " + extra[key] + "\n"
        header += "Cache-Control: no-store\n"
        header += 'Server: Simple-Python-Server\n'
        header += 'Connection: close\n\n'

        return header

    def handlerit(self, params, request_method):
        """
        This wat a sub method for a hard functionality

        Params: Not exactly sure !
        Return: the entire html response it seems
        """

        try:
            matchlist = []

            for handler in self.handlers:
                match = re.match(handler[0], self.splitpath(params))

                if match and handler[1] == request_method:
                    matchlist.append((handler, self.handlers[handler]))

            matchlist.sort(key=lambda x: len(x[0][0]), reverse=True)

            if matchlist:
                return matchlist[0]
            else:
                return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return {}, "", 200

    def dict_keys_uppercase(self, dict):
        """
        make all header keys uppercase so we always know
        for sure how to reach those.

        Params: a dicts
        Returns: the sam dict but this time all the keys are uppercase
        """
        return {key.upper(): val for key, val in dict.items()}

    def _handle_client(self):
        """
        This is the main loop of this class, receve user and feed him all requests

        Params: None
        Return: None
        """
        try:
            res = self.s.accept()
            client_sock = res[0]
            client_addr = res[1]
            PACKET_SIZE = 2048
            while True:
                data = client_sock.recv(PACKET_SIZE).decode()
                if not data:
                    break
                request_method = data.split(' ')[0]
                prarams = self.dictifyrequest(data)
                formses = "session={}".format(self.session)

                prarams.update({
                    'SAMESESS': "COOKIE" in prarams
                    and
                    formses == prarams['COOKIE']
                })

                if request_method.upper() == "POST":
                    if (
                        'CONTENT-TYPE' in prarams
                        and
                        prarams['CONTENT-TYPE'] == 'application/json'
                    ):
                        prarams.update({'POSTVALS': self.postparsejson(data)})
                    elif "CONTENT-LENGTH" in prarams and 'CONTENT-TYPE' in prarams and 'multipart/form-data' in prarams['CONTENT-TYPE']:
                        # hier moet een betere afhandeling komen van officiele post: Content-Type: multipart/form-data; boundary=X-INSOMNIA-BOUNDARY
                        newdatas = {}
                        for datas in client_sock.recv(prarams['CONTENT-LENGTH']).decode().split(prarams['CONTENT-TYPE'].split('=')[1]):
                            if '=' in datas:
                                cleaned = datas.replace('\r', '').replace('\n', '').replace('Content-Disposition: form-data; ', '').replace('name=\"', '').replace('--', '').split("\"")
                                newdatas.update({cleaned[0]:cleaned[1]})

                        prarams.update({'POSTVALS': newdatas})
                    else:
                        prarams.update({'POSTVALS': self.postparse(data)})


                handler = self.handlerit(prarams, request_method)

                if handler:
                    (
                        extraheaders,
                        response_data,
                        response_code
                    ) = handler[1](prarams)

                    extraheaders = self.dict_keys_uppercase(extraheaders)
                    if (
                        'CONTENT-TYPE' in extraheaders
                        and extraheaders['CONTENT-TYPE'] == 'application/json'
                    ):
                        response_data = json.dumps(response_data)

                    response_header = self._generate_headers(
                        extraheaders,
                        response_code
                    )
                else:
                    response_header = self._generate_headers({}, 404)
                    (
                        extraheaders,
                        response_data,
                        response_code
                    ) = self.fourzerofour(prarams)

                response = response_header.encode()

                if type(response_data).__name__ != "bytes":
                    response += response_data.encode()
                else:
                    response += response_data

                client_sock.send(response)
                client_sock.close()
                break
        except Exception as e:
            # DISABLEONBUILD 3
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            # ENABLEONBUILD 1
            # print("timeout web:", e)

    def set_fourzerofour(self, handler):
        self.fourzerofour = handler

    def splitpath(self, path):
        """
        Dis is een beetje kneus, ff refactoren

        params: als er get in path staat geeft dan het get deel terug , als er post in path staat geef dan post deel terug !
        return: de afzonderlijke delen !
        """
        if 'GET' in path:
            return path['GET'].split(' ')[0]
        elif 'POST' in path:
            return path['POST'].split(' ')[0]

    def unquote_to_bytes(self, string):
        """
        unquote_to_bytes('abc%20def') -> b'abc def'.

        Params: de string die geunquote moet worden
        return: de geunquote byte array !

        """
        # Note: strings are encoded as UTF-8.
        # This is only an issue if it contains
        # unescaped non-ASCII characters, which URIs should not.
        if not string:
            # Is it a string-like object?
            string.split
            return b''
        if isinstance(string, str):
            string = string.encode('utf-8')
        bits = string.split(b'%')
        if len(bits) == 1:
            return string
        res = [bits[0]]
        append = res.append
        # Delay the initialization of the table to not waste memory
        # if the function is never called
        # global _hextobyte
        if self._hextobyte is None:
            self._hextobyte = {
                (a + b).encode(): bytes.fromhex(a + b)
                for a in self._hexdig for b in self._hexdig
            }
        for item in bits[1:]:
            try:
                append(self._hextobyte[item[:2]])
                append(item[2:])
            except KeyError:
                append(b'%')
                append(item)
        return b''.join(res)

    def unquote(self, string, encoding='utf-8', errors='replace'):
        """
        Replace %xx escapes by their single-character equivalent.
        The optional encoding and errors parameters specify how to decode
        percent-encoded sequences into Unicode characters,
        as accepted by the bytes.decode() method.
        By default, percent-encoded sequences are decoded with UTF-8,
        and invalid sequences are replaced by a placeholder character.
        unquote('abc%20def') -> 'abc def'.


        """
        if '%' not in string:
            string.split
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'replace'

        newstring = ""
        for ch in string:
            if ch in list(self.letterrange("\x00", "\x7f")):
                newstring += ch
        string = newstring

        return self.unquote_to_bytes(string).decode(encoding, errors)

    def letterrange(self, start, stop):
        """
        generate a range of letters, i dont know what it is used for

        params: start, a letter to start with and b a letter to stop with
        return a generator, that you can use to get your letters !
        """
        for c in range(ord(start), ord(stop)+1):
            yield chr(c)

    def postparse(self, data):
        """
        parse post parameters as as dict

        Params: post data sring
        return: a dict of post data
        """
        # print(data.split("\n")[-1], "--------")
        return self.splitparams(data.split("\n")[-1])

    def postparsejson(self, data):
        """
        not sure this even works

        Params: also post string data
        return: also the same dict but in this case in json
        """
        return json.loads(data.split("\n")[-1])

    def numerfy(self, value):
        """
        will get the value detect if it is a number in the form of a string
        and convert it !

        Params: value in the form of a string
        Return: a number
        """
        newval = value.replace(',', '.').split('.')

        if len(newval) == 2 and newval[0].isdigit() and newval[1].isdigit():
            lenth = len(newval[1])
            decimal = int(newval[1])/(10**lenth)
            return float(newval[0]) + decimal

        if value.isdigit():
            return int(value)

        return value

    def dictifyrequest(self, data):
        """
        Will change the request params from text seperated by newlines
        to a dictionary

        Params: the request params in the sape of text
        return: the request params in the shape of a dict !
        """
        tempdict = {}

        for line in data.split('\n'):
            templist = line.split(" ", 1)
            if (len(templist) == 2):
                value = templist[1].replace("\r", "").rstrip().lstrip()
                value = self.numerfy(value)
                tempdict.update({
                    templist[0]
                    .upper()
                    .replace(":", "")
                    .rstrip()
                    .lstrip(): value
                })

        return tempdict
