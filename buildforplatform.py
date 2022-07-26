#!/usr/bin/env python

import sys
import os
import htmlmin
import shutil
import glob
from microbuild.microbuild import task
from microbuild.microbuild import build
import subprocess
# import simulator_version
import pycodestyle

from io import StringIO
from termcolor import colored
import pdoc
import requests
from bs4 import BeautifulSoup

os.environ["BUILDENV"] = 'yes'

# from simulator_version.unittests.testfilehelper import TestFileHelper
# from simulator_version.unittests.testmicrodnssrv import TestMicroDnsSrv
# from simulator_version.unittests.testmicrowebtemplate import TestMicroWebTemplate
# from simulator_version.unittests.testvalidator import TestValidator
# from simulator_version.unittests.testwebsettings import TestWebSettings


buildtemp = './build_temp/'
buildtemptemplates = './build_temp/templates/'
buildtemppartials = './build_temp/partials/'
buildtemplibs = './build_temp/lib/'

firmware = './latest_upy_firmware/'

buildraw = './microcontroller_version_build/'
buildlib = './microcontroller_version_build/lib/'
buildcss = "./microcontroller_version_build/static/css/"
buildimagesflags = "./microcontroller_version_build/static/images/flags/"
buildimagesicons = "./microcontroller_version_build/static/images/icons/"
buildjs = "./microcontroller_version_build/static/js/"
buildtemplates = "./microcontroller_version_build/templates/"
buildpartials = './microcontroller_version_build/partials/'

simulator = './simulator_version/'
simulatorlib = './simulator_version/lib/'
simulatortemplates = './simulator_version/templates/'
simulatorpartials = './simulator_version/partials/'
simulatorimagesflags = './simulator_version/static/images/flags/'
simulatorimagesicons = './simulator_version/static/images/icons/'
simulatorjs = './simulator_version/static/js/'
simulatorcss = './simulator_version/static/css/'

docdir = './simulator_version/documentation/'


def enable(numoaffected, textlist, rulenum):
    listoenables = {}
    listoenables.update({rulenum: ''})
    for value in range(int(numoaffected)):
        listoenables.update(
            {value+rulenum+1: textlist[value+rulenum+1].replace('#', '')}
        )
    return listoenables


def disable(numoaffected, textlist, rulenum):
    listodisables = {}
    listodisables.update({rulenum: ''})
    for value in range(int(numoaffected)):
        listodisables.update(
            {value+rulenum+1: "# " + textlist[value+rulenum+1]}
        )
    return listodisables


def remove(numoaffected, textlist, rulenum):
    listoremoves = {}
    for value in range(int(numoaffected)+1):
        listoremoves.update({value+rulenum: '<-rem->'})
    return listoremoves


def betweenpat(textlist, pat):
    removelist = {}
    firstindex = 0
    secondindex = 0

    for num, put in enumerate(textlist):
        if pat in put:
            if firstindex == 0:
                firstindex = num
            else:
                secondindex = num + 1
                for num in range(firstindex, secondindex):
                    removelist.update({num: '<-rem->'})
                firstindex = 0

    return removelist


def copyimageifintemplate(input):
    bss = BeautifulSoup(input, 'lxml')
    img_tags = bss.find_all('img')
    return [img['src'].split('/')[-1] for img in img_tags]


def transform(input):
    elements = {
        'ENABLEONBUILD': enable,
        'DISABLEONBUILD': disable,
        'REMOVEONBUILD': remove
    }
    splitted = input.split('\n')
    changes = {}

    for num, put in enumerate(splitted):
        if '#' in put:
            parts = [x for x in put.split(' ') if x]
            if len(parts) > 1 and parts[1] in elements:
                changes.update(elements[parts[1]](parts[2], splitted, num))
            elif num not in changes:
                changes.update({num: '<-rem->'})

    changes.update(betweenpat(splitted, '"""'))

    for key, change in changes.items():
        if key <= len(splitted):
            splitted[key] = change
    return "\n".join(splitted).replace('<-rem->\n', '')


def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)


@task()
def generate_documentation():
    if not os.path.isdir(docdir):
        os.makedirs(docdir)
    modules = ['./simulator_version/lib']
    context = pdoc.Context()
    modules = [
        pdoc.Module(mod, context=context) for mod in modules
    ]
    pdoc.link_inheritance(context)

    for mod in modules:
        for module_name, html in recursive_htmls(mod):
            fwrite = open(docdir + module_name.split('.')[-1] + ".html", 'w')
            fwrite.write(html)
            fwrite.close()


@task()
def do_unit_tests():
    """DONT USE"""
    print("gotta run all thos unit tests if you do no want to end uo in that 'special' place in hell !")
    import unittest
    allerrors = []

    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)

    # allerrors += runner.run(unittest.makeSuite(TestFileHelper)).errors
    # allerrors += runner.run(unittest.makeSuite(TestMicroDnsSrv)).errors
    # allerrors += runner.run(unittest.makeSuite(TestMicroWebTemplate)).errors
    # allerrors += runner.run(unittest.makeSuite(TestValidator)).errors

    for error in allerrors:
        print(error)

    if allerrors:
        print(colored("!!!! unit tests made errors, check it out !!!!", 'red'))
        raise ValueError(colored("!!!! unit tests made errors, check it out !!!!", 'red'))


@task()
def check_packages():
    """DONT USE"""
    import pkg_resources
    print(colored(
        "this will check if all the pipenv packages are installed that you need, if not it will let you know", 'blue'
    ))
    listofneeded = {
        "htmlmin",
        "termcolor",
        "requests",
        "unittest2",
        "html5lib",
        "bs4",
        "docutils",
        'zipp',
        'toml'
    }

    installed_packages = {
        d.project_name: d.version for d in pkg_resources.working_set
    }
    notinstalled = listofneeded - set(installed_packages.keys())
    if notinstalled:
        raise ValueError(colored("there are packacges that are not installed {}".format(notinstalled), 'red'))

@task()
def remove_build_dir():
    """ this will remove the build_dir"""
    import shutil
    print(colored("remove the temp build dir", 'blue'))
    shutil.rmtree(buildtemp)

@task()
def clean_old():
    """This will clean the old build environment files"""
    print(colored("print, it will take most files that where made by a build and remove the entire thing", 'blue'))
    import shutil
    try:
        shutil.rmtree(buildraw)
        # shutil.rmtree(buildtemp)
        shutil.rmtree(firmware)
    except:
        print(colored('Error while deleting directory', 'red'))


@task()
def make_dir_structure():
    """DONT USE"""
    print(colored("this will make the right dir tructure to put on you disk for simulating or on the esp for production, (you habe to put that stuff somewhere)", 'blue'))
    os.makedirs(buildlib)
    os.makedirs(firmware)
    os.makedirs(buildcss)
    os.makedirs(buildimagesflags)
    os.makedirs(buildimagesicons)
    os.makedirs(buildjs)
    os.makedirs(buildtemplates)
    os.makedirs(buildpartials)
    if not os.path.isdir(buildtemp):
        os.makedirs(buildtemp)
        os.makedirs(buildtemplibs)
        os.makedirs(buildtemptemplates)
        os.makedirs(buildtemppartials)

@task()
def test_code_style():


    for file in os.listdir(simulatorlib):
        if os.path.isfile(simulatorlib + file) and file.split('.')[1] == 'py':
            pep8style = pycodestyle.StyleGuide(quiet=True)
            result = pep8style.check_files([simulatorlib + file])
            # if len(result.lines) > 0 and result.total_errors > 0 and (result.total_errors / len(result.lines)) > 0.1:
            #     raise ValueError(colored(result.filename + " contains more than 10% errors per line of code, run pycodestyle", 'red'))

@task()
def gater_resources():
    """DONT USE"""
    import requests
    from bs4 import BeautifulSoup
    import gzip
    print(colored(
        "this is the part that will download the resources from the intertubes", 'blue'
    ))

    x = requests.get('https://mincss.com/entireframework.min.css')

    with gzip.open(buildtemp + 'entireframework.min.css.gz', 'wb') as f:
        f.write(str.encode(x.text))

    x = requests.get(
        'https://raw.githubusercontent.com/franciscop/umbrella/master/umbrella.min.js'
    )
    with gzip.open(buildtemp + 'umbrella.min.js.gz', 'wb') as f:
        f.write(str.encode(x.text))

    domainandshit = 'https://micropython.org'
    x = requests.get(domainandshit + '/download/esp32/')
    bss = BeautifulSoup(x.text, 'lxml')

    splitlinks = []
    for link in bss.find_all('a'):
        href = link.get('href')
        if '/resources/firmware' in href and 'unstable' not in href:
            splitlinks.append(href.split('-'))

    sorr = sorted(splitlinks, key=lambda tup: tup[2], reverse=True)

    if sorr:
        url = '-'.join(sorr[0])
        f = open(firmware + os.path.basename(url), 'w')
        x = requests.get(domainandshit + url)
        f.write(x.text)
        f.close()


@task()
def check_resource_exist():
    """DONT USE"""

    print(colored(
        "this will check if the resources such as js and css are downloadable on the internet", 'blue'
    ))
    x = requests.head('https://mincss.com/entireframework.min.css')
    mincssstatus = x.status_code
    x = requests.head(
        'https://raw.githubusercontent.com/franciscop/umbrella/master/umbrella.min.js'
    )
    umbrellajsstatus = x.status_code
    x = requests.head('https://micropython.org/download/esp32/')
    micropythonstatus = x.status_code

    if (
        mincssstatus != 200
        or umbrellajsstatus != 200
        or micropythonstatus != 200
    ):
        raise ValueError(colored("one or more resource are not online !, check this !", 'red'))


@task(check_resource_exist, gater_resources)
def compile_resources():
    """DONT USE"""
    print(colored(
        "this will compile the resouces, make them smaler, perhaps put some vars on some places, in the woest case scenarios", 'blue'
    ))
    print(colored(
        "it will also take the templates and the html and it will try to make those smaler as well", 'blue'
    ))

    listoffiles = []

    for file in os.listdir(simulatortemplates):
        fwrite = open(buildtemptemplates + file, 'w')
        fread = open(simulatortemplates + file, 'r')
        filecontent = fread.read()
        listoffiles += copyimageifintemplate(filecontent)
        minified = htmlmin.minify(filecontent)
        fwrite.write(minified)
        fread.close()

    for file in os.listdir(simulatorpartials):
        fwrite = open(buildtemppartials + file, 'w')
        fread = open(simulatorpartials + file, 'r')
        filecontent = fread.read()
        listoffiles += copyimageifintemplate(filecontent)
        minified = htmlmin.minify(filecontent)
        fwrite.write(minified)
        fread.close()

    for file in os.listdir(simulatorlib):
        if os.path.isfile(simulatorlib + file) and file.split('.')[1] == 'py':

            fwrite = open(buildtemplibs + file, 'w')
            fread = open(simulatorlib + file, 'r')
            fwrite.write(transform(fread.read()))
            fread.close()
            fwrite.close()

    for file in set(listoffiles):
        if os.path.exists(simulatorimagesflags + file):
            shutil.copy(simulatorimagesflags + file, buildimagesflags)

        if os.path.exists(simulatorimagesicons + file):
            shutil.copy(simulatorimagesicons + file, buildimagesicons)

@task()
def fill_dir_structure():
    """DONT USE"""
    print(colored(
        "this will fill the dir structure with the files that where copyed or generated, it will take them from everywhere and put them in the right place", 'blue'
    ))
    for filename in glob.glob(os.path.join(simulatorcss, '*.*')):
        shutil.copy(filename, buildcss)
    for filename in glob.glob(os.path.join(simulatorjs, '*.*')):
        shutil.copy(filename, buildjs)
    for filename in glob.glob(os.path.join(buildtemptemplates, '*.*')):
        shutil.copy(filename, buildtemplates)
    for filename in glob.glob(os.path.join(buildtemppartials, '*.*')):
        shutil.copy(filename, buildpartials)

    # moet er op de libs nog het een en ander gemuteerd worden ?, als in van simulator naar esp32 gaat direct goed ?
    for filename in glob.glob(os.path.join(buildtemplibs, '*.*')):
        if filename != buildtemplibs + 'connect.py' and filename != buildtemplibs + 'network.py':
            shutil.copy(filename, buildlib)

    shutil.copyfile(
        buildtemp + 'umbrella.min.js.gz', buildjs + 'umbrella.min.js.gz'
    )
    shutil.copyfile(
        buildtemp + 'entireframework.min.css.gz', buildcss + 'minframework.css.gz'
    )

    readmain = open(simulator + 'main.py', 'r')
    readviews = open(simulator + 'views.py', 'r')
    writemain = open(buildraw + 'main.py', 'w')
    writeviews = open(buildraw + 'views.py', 'w')

    writemain.write(transform(readmain.read()))
    writeviews.write(transform(readviews.read()))

    readmain.close()
    readviews.close()
    writemain.close()
    writeviews.close()

    os.mknod(buildraw + "config.json")


@task()
def generate_config():
    """DONT USE"""
    print(colored("this will generate the config file the main file that will differentiate for different platforms, for now esp32 and a simulator", 'blue'))


@task()
def check_size():
    """DONT USE"""
    print(colored(
        "this will check the final size of the build and will compare that size agans a known size of an esp32 filesystem, perhaps esp8266 even, who knows", 'blue'
    ))
    size = subprocess.run(
        ["du", "-sk", buildraw], capture_output=True).stdout.split(b'\t'
    )[0].decode("utf-8")

    esp_total_size = (4*1024)

    firmwaresize = subprocess.run(
        ["du", "-sk", firmware], capture_output=True).stdout.split(b'\t'
    )[0].decode("utf-8")

    print(colored(
        "After Upload there will be {}K space left !".format(esp_total_size - (int(firmwaresize) + int(size))), 'blue'
    ))


@task(do_unit_tests, check_packages, check_resource_exist, check_size)
def can_build():
    """This will run all the checks to see if it is possible to build in the first place !"""
    print(colored(
        "this will check if we can build in the first place with some primary checks", 'blue'
    ))


@task(can_build, clean_old, make_dir_structure, compile_resources, fill_dir_structure, generate_config, generate_documentation, test_code_style, remove_build_dir)
def build_esp32():
    """This will build the sourcecode for the esp 32"""
    print(colored(
        "this will be the wrapper that will build for the esp32, it will not do a whole lot itself", 'blue'
    ))


if __name__ == "__main__":
    build(sys.modules[__name__], sys.argv[1:])
