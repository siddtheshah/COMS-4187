from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
from collections import deque

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def scrapeBFS(start, domain, login=None):
    if domain[-1] != '/':
        domain += '/'

    p1 = re.compile('.*(?<!http).*')
    p2 = re.compile('http://' + domain + '*')

    phttp = re.compile('http')

    exploreQueue = deque()
    exploreQueue.append(start)

    visited = set()
    while exploreQueue:
        current = exploreQueue.popleft()
        print(current)
        print(p1.match(current))
        print(p2.match(current))

        if current not in visited:
            visited.add(current)
            if not phttp.match(current):
                current = 'http://' + domain + current
            digest = simple_get(current)
            if digest:
                html = BeautifulSoup(digest, 'html.parser')
                links = [a.get('href') for a in html.find_all('a', href=True)]
                #print(links)
                internal_links = set()
                internal_links = set(filter(lambda x : not(x.startswith('http')), links))# | set(filter(p2.match, links))
                print(internal_links)
                for link in internal_links:
                    if link not in visited:
                        exploreQueue.append(link)
    return visited





def test():
    domain = "localhost"
    url = "http://localhost/bWAPP/login.php"
    html = BeautifulSoup(simple_get(url), 'html.parser')
    links = [a.get('href') for a in html.find_all('a', href=True)]
    #print(links)

    p = '(?<!://)'
    pattern = re.compile(p+r'.*\.php\Z')
    internal_links = filter(pattern.match, links)
    print(internal_links)


print(scrapeBFS("http://localhost/bWAPP/portal.php", "localhost/bWAPP"))