import signal
import sys
import urlparse
import argparse
import requests

from bs4 import BeautifulSoup
from collections import deque


URLS = set()                # Unique set of all urls collected
VISITED_LINKS = set()       # For crawling a url only once
VERBOSE = False

def signal_handler(signal, frame):
    """exit gracefully on keybord interrupt"""
    print "\n\n[Stopped]"
    print "Found: %d links \n" % len(URLS)

    for link in URLS:
        print link
    sys.exit(0)

def logg(msg):
    """ print to screen based on VERBOSE toggling """
    if VERBOSE: print msg


def crawl(url, max_depth=10):
    """The main crawler function.

    Takes a url and max_depth as input parameters and returns a list of crawled
    urls. Urls beyond max_depth are not crawled, (default: 10).
    """
    host = get_host_name(url)   # For crawling same host urls
    depth = 0                   # Set the root depth to 0

    # add url to the url traversal queue, thus making it our starting url
    dq = deque()
    dq.append((url, depth))
    print 'Fetching urls...'
    print 'Press [Ctrl-C] to stop crawling anytime'

    while len(dq) != 0:
        # pop the the first url and crawl
        current_url, depth = dq.popleft()
        if depth > max_depth:
            continue

        logg('Crawling %s' % current_url)
        #print 'phew', current_url, check_if_not_visited(current_url),
        #check_if_same_host(host, current_url)

        if check_if_not_visited(current_url) and check_if_same_host(host, current_url):
            try:
                VISITED_LINKS.add(current_url)
                page_links = fetch_all_links(current_url)


                for link in page_links:
                    if link not in URLS:
                        # increase the depth of the link since it is found on an
                        # internal page
                        logg('Adding %s' % link)
                        dq.append((link, depth+1))
                        URLS.add(link)

            except Exception, e:
                pass
        else:
            continue

def fetch_all_links(url):
    """This function creates a request object and fetches the successive url"""

    url_list = []
    try:
        r = requests.get(url)
        if r.status_code == 200:

            logg('Fetching in page links...')
            #print r.status_code
            content = r.content
            soup = BeautifulSoup(content, "lxml")

            # scan for all anchor tags
            tags = soup('a')

            for a in tags:
                href = a.get("href")
                if href is not None:
                    new_url = urlparse.urljoin(url, href)
                    if new_url not in url_list:
                        url_list.append(make_clean_url(new_url))
            return url_list

        elif r.status_code == 403:
            print "Error: 403 Forbidden url"
        elif r.status_code == 404:
            print "Error: 404 URL not found"
        else:
            print "Make sure you have everything correct."

    except requests.exceptions.ConnectionError, e:
        print "Oops! Connection Error. Try again"

def check_if_same_host(host, url):
    """Return True if URL belongs to the same hostname"""
    # print '\nchecking same origin:', host, get_host_name(url)

    if host == get_host_name(url):
        return True
    return False

def check_if_not_visited(url):
    """Returns True if the URL has not been visited already"""
    return (url not in VISITED_LINKS)

def get_host_name(url):
    """Returns the netlock/ hostname of the url from urlparsed object"""
    return urlparse.urlparse(url)[1]

def make_clean_url(url):
    """Returns the base url and strips out querystring parameteres"""
    return urlparse.urldefrag(url)[0]


if __name__ == '__main__':
    try:
        # handle SIGINT
        signal.signal(signal.SIGINT, signal_handler)

        parser = argparse.ArgumentParser(
            prog="crawler",
            description="A basic implementation of a web crawler written in python.",
            epilog="For more information see http://github.com/shashankgroovy/crawler")

        parser.add_argument("url", help="the url to crawl")
        parser.add_argument("-d", "--depth", type=int, default=10,
                            help="set the max_depth for crawling")
        parser.add_argument('-v', '--verbose', action="store_true",
                           help="Toggle verbose on (default is off)")

        args = parser.parse_args()

        VERBOSE = args.verbose
        url = args.url

        if args.depth:
            depth = args.depth
        else:
            depth = 10

        if len(sys.argv) == 1:
            parser.print_help()

        crawl(url, depth)

        print "\n----------------------------------------"
        print "Found: %d links \n" % len(URLS)
        for link in URLS:
            print link

    except KeyboardInterrupt:
        pass
