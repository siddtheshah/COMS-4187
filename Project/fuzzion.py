from requests import *
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import urllib2
import urllib
import urlparse
import fuzzStrings
import hashlib
import os
import shutil
import sys
from optparse import OptionParser
#import webScrape

parser = OptionParser()
parser.add_option("-b", "--bug", type="int", dest="bug", help="bug # on the bWAPP site (int)")
parser.add_option("-q", "--query-output", type="string", dest="queryDir", default="run", help="Where to store successful malicious queries")
parser.add_option("-r", "--page-output", type="string", dest="pageDir", default="returned", help="Where to store returned pages")
parser.add_option("-u", "--user", type="string", dest="user", default= "bee", help="preferred bWAPP username")
parser.add_option("-p", "--password", type="string", dest="pwd", default="bug", help="password for account")
parser.add_option("-s", "--security_level", type="string", dest="sec", default=0, help="bWAPP security_level")
parser.add_option("-f", "--fuzz_set", type="int", dest="fuzz", default=0, help="Set of fuzzing inputs")
parser.add_option("-i", "--field_input", type="string", dest="inp", default="", help="File for manually set field inputs (format is 'field':'data')")
(options, args) = parser.parse_args()

#print options
bug = options.bug
# 13 for get/search
# 15 for post/search
# 39 for password attacks
# 41 for 
assert isinstance(bug, int), "Integer not entered, aborted"

flicker = fuzzStrings.Flicker(1)

site = 'http://localhost/bWAPP/login.php'

in_data = {}
extra_fields = []
if options.inp != "":
    try:
        f = open(os.getcwd() + "/" + options.inp, "r")
        for l in f:
            x, y = l.rstrip().split(":")
            if y == '':
                extra_fields.append(x)
            else:
                in_data[x] = y
    except:
        print "Input file doesn't exist or is badly formatted"
        sys.exit()
#print extra_fields
queriesDir = os.getcwd() + "/" + options.queryDir + "/"
if os.path.exists(queriesDir):
    ans = raw_input("Overwrite query directory? (y/n) ")
    if ans == 'y':
        shutil.rmtree(queriesDir)
    else:
        print "Overwrite not confirmed, aborted"
        sys.exit()

pagesDir = os.getcwd() + "/" + options.pageDir + "/"
if os.path.exists(pagesDir):
    ans = raw_input("Overwrite page directory? (y/n) ")
    if ans == 'y':
        shutil.rmtree(pagesDir)
    else:
        print "Overwrite not confirmed, aborted"
        sys.exit()

os.makedirs(queriesDir)
os.makedirs(pagesDir)


# resultsDir = os.getcwd() + "/" + options["destDir"] + "/"
# if not os.path.exists(resultsDir):
#     os.makedirs(resultsDir)
# else:
#     shutil.rmtree(resultsDir)
#     os.makedirs(resultsDir)

initialLogin = {'login' : options.user, 'password' : options.pwd , 'security_level' : options.sec, 'form' : 'submit'}

with requests.Session() as s:
    r = s.post('http://localhost/bWAPP/login.php', data=initialLogin)

    # choosing page to inject
    choice = { 'bug' : bug, 'form' : 'submit'}
    hackpage = s.post(r.url, data=choice)
    html = BeautifulSoup(hackpage.text, 'html.parser')

    # if the url directs us to some page with params, we definitely want to mess with those
    param_dict = urlparse.parse_qs(urlparse.urlparse(hackpage.url).query)
    url_inputs = param_dict.items()

    # Generally only interested in the first form that appears on the page.
    inputs = url_inputs
    j = hackpage.url.find("?")
    if j != -1:
        baseUrl = hackpage.url[:j]
    else:
        baseUrl = hackpage.url
    print "Fuzzing " + baseUrl
    main = html.find(id="main")
    #forms = html.find_all('form')
    #form = forms[0] # hack
    form = main.find('form')

    if form:
        method = form.get('method')
        text_inputs = [(a.get('name'), a.get('value')) for a in form.find_all('input')]
        select_inputs = [(a.get('name'), a.get('value')) for a in form.find_all('select')]
        button_inputs = [(a.get('name'), a.get('value')) for a in form.find_all('button')]
        atext_inputs = [(a.get('name'), a.get('value')) for a in form.find_all('textarea')]
    else:
        method = "GET"
        text_inputs = []
        select_inputs = []
        button_inputs = []
        atext_inputs = []

    inputs = inputs + text_inputs + select_inputs + button_inputs + atext_inputs
    #print(inputs)
    assert len(inputs) + len(extra_fields) > 0, "No inputs found for this bug"
    noDefaults = []
    fixed = []
    data = in_data.copy()
    for x, y in inputs:
        if x in in_data.keys():
            data[x] = in_data[x]
            fixed.append(x)
        else:
            data[x] = y
            if not y:
                noDefaults.append(x)
                data[x] = '0' #placeholder so the form actually submits

    for x in extra_fields: # extra fields functionality
        if x not in data:
            data[x] = '0'
    print "Default data is: "
    print(data)
    fzs = fuzzStrings.getFuzzFromSet(options.fuzz)

    # stuff fields with normal-ish input to start with, since we want to fuzz 1 by 1.
    pageHashes = set()

    #print(data)
    #testables = data.keys()
    testables = set(noDefaults)
    testables.update([x for x, y in text_inputs]) 
    testables.update([x for x, y in atext_inputs]) # want to fuzz all text inputs guaranteed
    testables.update([x for x, y in select_inputs])
    testables.update([x for x, y in url_inputs])
    testables.update(extra_fields)
    for rem in fixed:                              # except the fixed stuff.
        testables.remove(rem)

    showStrs = "\nInput fields are: \n" 
    for test in list(testables):
        showStrs += "\n" + test
    print showStrs + "\n"
    html_index = 0
    for name in testables:
        f = open(queriesDir + name + ".txt", "w+")
        input_dict = data.copy()
        for fuzzString in fzs:
            # print(fuzzString)
            # if fuzzString == '1':
            #     b = 0
            sys.stdout.write(flicker.update() + '\r')
            sys.stdout.flush()
            input_dict[name] = fuzzString
            #print fuzzString
            #print input_dict

            try:
                if method == "GET":
                    r = s.get(baseUrl, params=input_dict, timeout=5)
                elif method == "POST":
                    r = s.post(hackpage.url, data=input_dict, timeout=5)
            except:
                f.write("" + str(html_index) + ":" + fuzzString + "\n") # stuff that causes timeout should be logged
                p = open(pagesDir + str(html_index) + ".timeout", 'w')
                p.write("Timeout occurred")
                p.close()
                html_index += 1
                continue

            #print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            [sp.extract() for sp in soup(['style', 'script', '[document]', 'head', 'title'])]
            text = soup.getText()

            #text = r.text.lower()
            formSuccess = text.find('error') == -1 and text.find('invalid') == -1 and text.find('incorrect') == -1# basic form errors are uninteresting

            # check for perfect query echos
            if len(fuzzString) > 40:
                truncString = fuzzString[:40]
            else:
                truncString = fuzzString

            if len(truncString) > 4:
                noEcho = text.find(truncString.decode('utf8')) == -1 # echoing input is not interesting
            else:
                noEcho = True
            #print(hasError)
            quickHash = hashlib.sha256(r.text.encode('ascii', 'ignore'))
            h = int(quickHash.hexdigest(), 16) % 256 # reducing memory usage
            #print h
            #print h, formSuccess, noEcho
            if h not in pageHashes and formSuccess and noEcho: # a new, interesting result
                pageHashes.add(h)
                f.write("" + str(html_index) + ":" + fuzzString + "\n")
                p = open(pagesDir + str(html_index) + ".html", 'w')
                p.write(r.text)
                p.close()
                html_index += 1

        f.close()

print("" + str(html_index) + " Interesting Results Found")
