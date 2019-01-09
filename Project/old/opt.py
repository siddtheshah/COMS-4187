# from optparse import OptionParser
# #import webScrape

# parser = OptionParser()
# parser.add_option("-b", "--bug", type="int", dest="bug")
# parser.add_option("-o", "--output", type="string", dest="destDir")
# (options, args) = parser.parse_args()
# print(args)
# print(options)

from requests import *
import requests
from requests.exceptions import RequestException

with requests.Session() as s:
    r = s.get('http://localhost/bWAPP/login.php')
    f = open('2.html', 'w')
    f.write(r.text)