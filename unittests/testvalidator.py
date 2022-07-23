import unittest

# from lib.validator import validator

import unittest, os


if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.validator import validator
else:
    from lib.validator import validator

class TestValidator(unittest.TestCase):

    def test_validator_numeric(self):
        valida = validator()
        formdata = {'aaps':'G', 'aaps_validator':'numeric'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])

        formdata = {'aaps':'235', 'aaps_validator':'numeric'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

    def test_validator_required(self):
        valida = validator()
        formdata = {'aaps':'', 'aaps_validator':'required'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])

        formdata = {'aaps':'EGEG', 'aaps_validator':'required'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

    def test_validator_alpha(self):
        valida = validator()
        formdata = {'aaps':'234', 'aaps_validator':'alpha'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])

        formdata = {'aaps':'EGEG', 'aaps_validator':'alpha'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

    def test_validator_biggerthen(self):
        valida = validator()
        formdata = {'aaps':'23', 'aaps_validator':'biggerthen=5'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

        formdata = {'aaps':'EGfefEG', 'aaps_validator':'biggerthen=5'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

        formdata = {'aaps':'2', 'aaps_validator':'biggerthen=5'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])

        formdata = {'aaps':'EGfe', 'aaps_validator':'biggerthen=5'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])


    def test_validator_smalerthen(self):
        valida = validator()
        formdata = {'aaps':'3', 'aaps_validator':'smalerthen=5'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

        formdata = {'aaps':'sdf', 'aaps_validator':'smalerthen=5'}
        valida.handleform(formdata)
        self.assertFalse(valida.get_errors()[0])

        formdata = {'aaps':'20', 'aaps_validator':'smalerthen=5'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])

        formdata = {'aaps':'EGwfseffe', 'aaps_validator':'smalerthen=5'}
        valida.handleform(formdata)
        self.assertTrue(valida.get_errors()[0])
