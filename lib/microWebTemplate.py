import re


class MicroWebTemplate:
    """
    This class will do micropython templating.
    It needs some refactoring
    """

    # INSTRUCTION_PYTHON = 'py'
    # INSTRUCTION_IF = 'if'
    # INSTRUCTION_ELIF = 'elif'
    # INSTRUCTION_ELSE = 'else'
    # INSTRUCTION_FOR = 'for'
    # INSTRUCTION_END = 'end'
    # INSTRUCTION_INCLUDE = 'include'
    #
    # MESSAGE_TEXT = ''
    # MESSAGE_STYLE = ''

    # refactor self._instructions naar directe upper text vor keys
    # kijken of we de exceptions kunnen dumpen, of wellicht minder
    # _processToken kan worden opgedeelt in een tal fucnties
    # het lijkt erop dat de begin end detectie altijd opdezelfde manier wordt gedaan, hoe exact weet ik niet, maar als dit kan worden onderbebracht in een apparte functie
    # de indent riedel, kan worden teruggebrancht tot een functie
    # remove identifier, validate !
    # wil ik de py functie hier in hebben ?, nogal groot en gevaarlijk !
    # de for instructie split voor dicts en list is nu nogal lomp gedaan, kijken of dat anders kan !

    def __init__(self, tokenopen="{{", tokenclose="}}", filepath='./'):

        self.tokenopen = tokenopen
        self.tokenclose = tokenclose
        self.tokenopenlen = len(tokenopen)
        self.tokencloselen = len(tokenclose)
        self._filepath = filepath

        self.internationaliser = None
        self._pos = 0
        self._line = 1
        self._pyGlobalVars = {}
        self._pyLocalVars = {}
        self._rendered = ''
        self._instructions = {
            'py': self._processInstructionPYTHON,
            'if': self._processInstructionIF,
            'elif': self._processInstructionELIF,
            'else': self._processInstructionELSE,
            'for': self._processInstructionFOR,
            'end': self._processInstructionEND,
            'include': self._processInstructionINCLUDE,
        }

    def SetInternationaliser(self, internationaliser):
        self.internationaliser = internationaliser

    def Execute(self, code, pyGlobalVars=None, pyLocalVars=None):
        """
        This function will parse the template and output html
        """
        self._pos = 0
        self._code = code

        self._endPos = len(self._code)-1
        if pyGlobalVars:
            self._pyGlobalVars = pyGlobalVars
        if pyLocalVars:
            self._pyLocalVars = pyLocalVars

        self._parseCode( execute=True)

        if self.internationaliser:
            self._rendered = self.internationaliser.translate(self._rendered)

        return self._rendered


    def _parseCode(self, execute):
        """
        This function will also parse the template to html but will not
        give exceptions.
        """

        self._rendered = ''
        newTokenToProcess = self._parseBloc(execute)


    def _parseBloc(self, execute):
        """
        I guess it will parse a block of python _code
        """
        while self._pos <= self._endPos:

            c = self._code[self._pos]
            if (
                c == self.tokenopen[0]
                and
                self._code[self._pos: self._pos + self.tokenopenlen]
                ==
                self.tokenopen
            ):
                self._pos += self.tokenopenlen
                tokenContent = ''
                x = self._pos
                while True:

                    c = self._code[x]
                    if (
                        c == self.tokenclose[0]
                        and
                        self._code[x: x + self.tokencloselen]
                        ==
                        self.tokenclose
                    ):
                        self._pos = x + self.tokencloselen
                        break
                    elif c == '\n':
                        self._line += 1
                    tokenContent += c
                    x += 1

                newTokenToProcess = self._processToken(tokenContent, execute)

                if newTokenToProcess is not None:
                    return newTokenToProcess
                continue

            elif c == '\n':
                self._line += 1
            if execute:
                self._rendered += c
            self._pos += 1

        return None

    def _processToken(self, tokenContent, execute):
        """
        It means to get all between {{ and }} and process that
        """
        tokenContent = tokenContent.strip()
        parts = tokenContent.split(' ', 1)
        instructName = parts[0].strip()
        instructBody = parts[1].strip() if len(parts) > 1 else None

        newTokenToProcess = None
        if instructName in self._instructions:
            newTokenToProcess = self._instructions[instructName](instructBody, execute)

        elif execute:
            try:
                tokenContent = tokenContent.replace(']', '').split('[')

                if (
                    tokenContent[0] in self._pyGlobalVars
                    or
                    tokenContent[0] in self._pyLocalVars
                ):
                    if len(tokenContent) == 1:
                        s = str(eval(
                            tokenContent[0],
                            self._pyGlobalVars,
                            self._pyLocalVars
                        ))
                    elif len(tokenContent) == 2:
                        tokenContent = tokenContent[0] + "['" + tokenContent[1] + "']"

                        s = str(eval(
                            tokenContent,
                            self._pyGlobalVars,
                            self._pyLocalVars
                        ))
                    else:
                        s = tokenContent[0] + " not in variables"
                    self._rendered += s
                else:
                    self._rendered += tokenContent[0] + ' Unknown VAR'

            except Exception as ex:
                print(es)
        return newTokenToProcess

    def _processInstructionPYTHON(self, instructionBody, execute):

        pyCode = ''
        while True:

            c = self._code[self._pos]
            if c == (
                self.tokenopen[0]
                and
                self._code[self._pos: self._pos + self.tokenopenlen]
                ==
                self.tokenopen
            ):
                self._pos += self.tokenopenlen
                tokenContent = ''
                x = self._pos
                while True:

                    c = self._code[x]
                    if (
                        c == self.tokenclose[0]
                        and
                        self._code[x: x + self.tokencloselen]
                        ==
                        self.tokenclose
                    ):
                        self._pos = x + self.tokencloselen
                        break
                    elif c == '\n':
                        self._line += 1
                    tokenContent += c
                    x += 1
                tokenContent = tokenContent.strip()
                if tokenContent == 'end':
                    break

            elif c == '\n':
                self._line += 1
            if execute:
                pyCode += c
            self._pos += 1
        if execute:
            lines = pyCode.split('\n')
            indent = ''
            for line in lines:
                if len(line.strip()) > 0:
                    for c in line:
                        if c == ' ' or c == '\t':
                            indent += c
                        else:
                            break
                    break
            pyCode = ''
            for line in lines:
                if line.find(indent) == 0:
                    line = line[len(indent):]
                pyCode += line + '\n'
            try:
                exec(pyCode, self._pyGlobalVars, self._pyLocalVars)
            except Exception as ex:
                print(ex)
        return None

    def _processInstructionIF(self, instructionBody, execute):
        """
        The part that will process in template if else _code
        """

        if instructionBody is not None:
            if execute:
                try:
                    if (' ' not in instructionBody) and \
                       ('=' not in instructionBody) and \
                       ('<' not in instructionBody) and \
                       ('>' not in instructionBody) and \
                       (instructionBody not in self._pyGlobalVars) and \
                       (instructionBody not in self._pyLocalVars):

                        result = False
                    else:
                        result = bool(
                            eval(
                                instructionBody,
                                self._pyGlobalVars,
                                self._pyLocalVars
                            )
                        )

                except Exception as ex:
                    print(ex)
            else:
                result = False
            newTokenToProcess = self._parseBloc(execute and result)
            if newTokenToProcess is not None:
                if newTokenToProcess == 'end':
                    return None
                elif newTokenToProcess == 'else':
                    newTokenToProcess = self._parseBloc(execute and not result)
                    if newTokenToProcess is not None:
                        if newTokenToProcess == 'end':
                            return None

                elif newTokenToProcess == 'elif':
                    self._processInstructionIF(
                        self._elifInstructionBody,
                        execute and not result
                    )
                    return None


    def _processInstructionELIF(self, instructionBody, execute):
        """
        For the if and else and ifelse code processing in the template
        this will handle the elif parts.
        """

        self._elifInstructionBody = instructionBody
        return 'elif'

    def _processInstructionELSE(self, instructionBody, execute):
        """
        For the if and else and ifelse code processing in the template
        this will handle the else parts.
        """

        return 'else'

    def _processInstructionFOR(self, instructionBody, execute):
        """
        You can use for loops in the templates
        this is the method that handle those for loops.
        """
        if instructionBody is not None:
            parts = instructionBody.split(' ', 1)

            identifier = parts[0].strip().split(',')
            parts = parts[1].strip().split(' ', 1)

            if parts[0] == 'in' and len(parts) > 1:
                expression = parts[1].strip()
                newTokenToProcess = None
                beforePos = self._pos

                # if execute and (expression in self._pyGlobalVars or expression in self._pyLocalVars):
                if execute:
                    try:
                        result = eval(
                            expression,
                            self._pyGlobalVars,
                            self._pyLocalVars
                        )
                    except Exception as ex:
                        print(ex)

                if execute and len(result) > 0:

                    if result.__class__.__name__ == 'list' and len(identifier) == 1:
                        for x in result:
                            self._pyLocalVars[identifier[0]] = x
                            self._pos = beforePos
                            newTokenToProcess = self._parseBloc(True)
                            if newTokenToProcess != 'end':
                                break
                    elif len(identifier) == 2:
                        for x, y in enumerate(result):
                            self._pyLocalVars[identifier[0]] = x
                            self._pyLocalVars[identifier[1]] = y
                            self._pos = beforePos
                            newTokenToProcess = self._parseBloc(True)
                            if newTokenToProcess != 'end':
                                break
                else:
                    newTokenToProcess = self._parseBloc(False)
                if newTokenToProcess is not None:
                    if newTokenToProcess == 'end':
                        return None



    def _processInstructionEND(self, instructionBody, execute):
        """
        The end tag }} will be handles by this method
        """
        return 'end'

    def _processInstructionINCLUDE(self, instructionBody, execute):
        """
        This is the code that will handle the include statements
        in the templates.
        """
        filename = instructionBody.replace('"', '').replace("'", '').strip()

        idx = self._filepath.rindex('/')
        if idx >= 0:
            filename = self._filepath[:idx+1] + filename

        with open(filename, 'r') as file:
            includeCode = file.read()
            self._code = (
                self._code[:self._pos] +
                includeCode +
                self._code[self._pos:]
            )
            self._endPos += len(includeCode)
