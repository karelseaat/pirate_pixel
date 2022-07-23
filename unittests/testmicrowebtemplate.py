import unittest, os


if 'BUILDENV' in os.environ and os.environ["BUILDENV"]:
    from simulator_version.lib.microWebTemplate import MicroWebTemplate
    patho = './simulator_version/'
else:
    patho = './'
    from lib.microWebTemplate import MicroWebTemplate

class TestMicroWebTemplate(unittest.TestCase):

    def test_var_show(self):
        templatevars = {'var1': 'aaa', 'var2': 'bbb'}
        tmpl = "<div class={{ var1 }}>{{ var2 }}</div>"
        mWebTmpl = MicroWebTemplate()
        self.assertTrue(mWebTmpl.Execute(tmpl, templatevars) == "<div class=aaa>bbb</div>")

    def test_include(self):
        vars = {'pagetitle':"it is a test", 'breadcrumbs':{'lol':'klont', 'lel':'ladida'}}
        tmpl = "<div>{{ include partials/navigation_partial.html }}</div>"
        mWebTmpl = MicroWebTemplate(filepath='./simulator_version/')
        transformed = mWebTmpl.Execute(tmpl, vars)
        self.assertTrue(len(transformed) == 221)
        self.assertTrue("lol" in transformed)
        self.assertTrue("klont" in transformed)
        self.assertTrue("it is a test" in transformed)
