import sys
import urlparse

import requests
from bs4 import BeautifulSoup
from collections import deque


URLS = set()                # Unique set of all urls collected
VISITED_LINKS = set()       # Crawl a url only once

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

    while len(dq) != 0:
        # pop the the first url and crawl
        current_url, depth = dq.popleft()
        if depth > max_depth:
            continue

        #print 'visited links', VISITED_LINKS

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
                        # print 'Adding %s' % link
                        dq.append((link, depth+1))
                        URLS.add(link)

            except Exception, e:
                pass
        else:
            continue
    return URLS


def fetch_all_links(url):
    """This function creates a request object and fetches the successive url"""

    url_list = []
    try:
        r = requests.get(url)
        if r.status_code == 200:

            #print "Fetching url..."
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

    except requests.exceptions.ConnectionError:
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
    url = sys.argv[1]

    links = crawl(url)
    print "\nFound %d links \n" % len(links)
    for link in links:
        print link
