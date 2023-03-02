
import re


class validator(object):
    """
    This class will validate form values, but will actualy validate dictionarys.

    Params:

    Return:
    """
    validators = {}
    results = {}
    values = {}

    def __init__(self):
        self.validators = {
            "notrequired": (self.notrequired, ""),
            "required": (self.required, "field is required"),
            'alpha': (self.alpha, "field should be alpha only"),
            'numeric': (self.numeric, "field should be numeric"),
            'biggerthen': (self.biggerthen, "field should be bigger than"),
            'smalerthen': (self.smalerthen, "field should be smaler than")
        }

    def handleform(self, formdata):
        """
        This method will validate a form if you added form validation
        fields to the formdata.
        this could use some refactoring since there is duplicate code in here !

        Params: fom data in the form of a dict
        Return: None
        """
        results = {}
        keyvals = [(v, k) for (k, v) in formdata.items() if k.endswith("_validator")]
        if keyvals:
            for keyval in keyvals:
                if keyval[1].split('_')[0] in formdata:
                    validatorresults = []
                    for row in keyval[0].replace(' ', '').replace('%7C','|').replace('%3D','=').split('|'):
                        extraparam = None
                        if "=" in row:
                            total = row.split('=')
                            row = total[0]
                            extraparam = total[1]
                        if row in self.validators:
                            originalval = formdata[keyval[1].split('_')[0]]
                            self.values.update({keyval[1].split('_')[0]: originalval})
                            if extraparam:
                                message = self.validators[row][0](
                                    self.validators[row][1],
                                    originalval,
                                    extraparam
                                )
                            else:
                                message = self.validators[row][0](
                                    self.validators[row][1],
                                    originalval
                                )
                        if message:
                            validatorresults.append(message)

                self.results.update({keyval[1].split('_')[0]: validatorresults})

    def get_values(self):
        return self.values

    def get_errors(self):
        """
        Get all the errors in the validation and return them as a list.

        Params: None
        Return: A list of Booleans True if error False if not error
        """
        res = []
        for key, val in self.results.items():
            res.append(len(val) > 0)
        return res

    def get_inv_errors(self):
        """
        Get all the errors in the validation and return them as a list. inverted

        Params: None
        Return: A list of Booleans False if error True if not error
        """
        res = []
        for key, val in self.results.items():
            res.append(not bool(val))
        return res

    def error_free(self):
        """
        Get all the errors in the validation and return them as a list. inverted

        Params: None
        Return: A list of Booleans False if error True if not error
        """
        return all(self.get_inv_errors())

    def get_validated(self):
        """
        This hs the wrong name of the wrong functionality, it prints a list of the results of the validations

        Params: None
        Return: None
        """
        print(self.results)

    def get_results(self):
        """
        Get the results of the validation and return those as a dict. fieldname: result

        Params: None
        Return: a dict with the field names as keys and the results as values
        """
        returnres = {}
        for key, val in self.results.items():
            if val:
                returnres.update({key: ",".join(val)})
            else:
                returnres.update({key: ""})
        return returnres

    def handle_dict(self, datadict, filterdict):
        """
        Validate not form but a dictionarys
        quite sure this could also be refactored !

        Params: datadict a dict with the fieldnames and data, filterdict of fields to use
        Return: results  ???
        """
        results = {}
        for key, filters in filterdict.items():
            validatorresults = []
            for filteritem in filters:
                extraparam = None
                if "%3D" in filteritem:
                    total = filteritem.split('%3D')
                    filteritem = total[0]
                    extraparam = total[1]
                if filteritem in self.validators:
                    if extraparam:
                        message = self.validators[filteritem][0](
                            self.validators[filteritem][1],
                            datadict[key],
                            extraparam
                        )
                    else:
                        message = self.validators[filteritem][0](
                            self.validators[filteritem][1],
                            datadict[key]
                        )
                    if message:
                        validatorresults.append(message)

            results.update({key: validatorresults})
        return results

    def notrequired(self, orimesg, value):
        return None

    def required(self, orimesg, value):
        """
        A validation method to see if it form field was filled.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        if not bool(value):
            return orimesg

    def alpha(self, orimesg, value):
        """
        A validation method to see if a form field consists of
        alphabetical chars.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        if not value.isalpha():
            return orimesg

    def numeric(self, orimesg, value):
        """
        A validation to see if a form field consists of numerical chars.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        if not value.replace('.', '').isdigit():
            return orimesg

    def biggerthen(self, orimesg, value, max):
        """
        a validation method to see is a form field has a value that is bigger
        than test value.
        A number that is bigger then if a string that is longer then.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        if value.isdigit():
            if not int(value) > int(max):
                return orimesg
        else:
            if not len(value) > int(max):
                return orimesg

    def smalerthen(self, orimesg, value, min):
        """
        A validation method to see is a form field has a value that is
        smaler than test value.
        A number that is smaler then if a string that is shorter then.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        if value.isdigit():
            if not int(value) < int(min):
                return orimesg
        else:
            if not len(value) < int(min):
                return orimesg

    def domain(self, orimesg, value):
        """
        A validation method to see is a form field consists of a domain.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        searchstr = r"^[a-zA-Z0-9][a-zA-Z0-9-_]{0,61}[a-zA-Z0-9]{0,1}\.([a-zA-Z]{1,6}|[a-zA-Z0-9-]{1,30}\.[a-zA-Z]{2,3})$"
        if not re.search(value, searchstr):
            return orimesg

    def ip(self, orimesg, value):
        """
        A validation method to see is a form field consists of a ip address.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        searchstr = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if not re.search(value, searchstr):
            return orimesg

    def email(self, orimesg, value):
        """
        A validation method to see if a form field consists of an email address.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        searchstr = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.search(value, searchstr):
            return orimesg

    def datumnl(self, orimesg, value):
        """
        A validation method to see if a form field consists of a datum
        not sure what the datum format is yet.

        Params: orimesg, the message you get when if fails, value is the value to check
        Return: True if things go wrong, False if things go well
        """
        searchstr = r"([12]\d{3}[-:](0[1-9]|[12]\d|3[01])[-:](0[1-9]|1[0-2]))"
        if not re.search(value, searchstr):
            return orimesg

#Ende van de file
