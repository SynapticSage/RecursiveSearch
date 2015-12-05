# Ryan Young -- modifying to better recurse web sites ... exhibits behavior I'm not all to fond of in it's normal state!
# I'd like to be able to use this to recursively search, say a faculty page, to quickly identify faculty I may not be
# aware of with Nature or Neuron or Nature Neuroscience papers.

# CODE MODIFIED FROM http://code.activestate.com/recipes/577388-website-text-search/

# websiteTxtSearcher.py
# Searches a website recursively for any given string.
# FB - 201009105

# TODO something's wrong with the code's endogenous level systeM! it's not counting down levels from the root url.

import urllib2
from os.path import basename
import urlparse
from BeautifulSoup import BeautifulSoup # for HTML parsing

global hitList
hitList=[]
global urlList
urlList = []
global rootUrl

# recursively search starting from the root URL
def searchUrl(url, level, searchText, stayInOriginalRoot = False): # the root URL is level 0

    # do not go to other websites
    global website
    netloc = urlparse.urlsplit(url).netloc.split('.')
    if netloc[-2] + netloc[-1] != website:
        return

    # if we desire to stay witihin the rooturl's path, then return whenever we're not
    if stayInOriginalRoot :
        if url.find(rootUrl) == -1:
            return

    global urlList
    if url in urlList: # prevent using the same URL again
        return

    try:
        urlContent = urllib2.urlopen(url).read()
        urlList.append(url)
    except:
        return

    print "About to search " + url + " at level " + str(3-level) + "\n\n"

    soup = BeautifulSoup(''.join(urlContent))
    # remove script tags
    c=soup.findAll('script')
    for i in c:
        i.extract()
    # get text content of the URL
    try:
        body_texts = soup.body(text=True)
    except:
        return
    text = ''.join(body_texts)

    # search
    if text.find(searchText) > -1:
        print url
        print
        hitList.append(url)

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:

                    linkUrl = linkTag['href']  # FIXED: error when searching pages that are supposed to concatonate onto main address!!
                    # Debug part 1
                    print "\n\n --------------------------------------"
                    print 'Link url before = ' + linkUrl

                    # Concatonate onto address if extended link
                    if (linkUrl.find('/') == -1 or linkUrl.find('/') == 0) and linkUrl.find('.html') == -1: #TODO still not perfect, because should append found string to the raw domain name that indexes server's root directory
                        main_url = ''
                        for n in netloc:
                            main_url = main_url + n + '.'

                        if linkUrl.find('/') == 0 :
                            main_url = main_url[0:-1]
                        else :
                            main_url = main_url[0:-1] + '/'

                        linkUrl = 'http://' + main_url + linkUrl

                    # Debug part 2
                    print 'Link url after = ' + linkUrl
                    print 'Levels left before exit = ' + level
                    print "---------------------------------------- \n\n"

                    searchUrl(linkUrl, level - 1, searchText, stayInOriginalRoot)

                except:
                    pass



######### MAIN SCOPE OF CODE ##########

print "Hello world! about to start ... "

rootUrl = 'http://blah.edu/faculty'             # URL TO SEARCH!!!
print "About to search " + rootUrl
netloc = urlparse.urlsplit(rootUrl).netloc.split('.')   # root strings of domain stored to be sure we stay in the domain
global website                                          # initialize object that will keep track of parent domain
website = netloc[-2] + netloc[-1]                       # blahblah.foobar ... stores two key parts of server domain
searchUrl(rootUrl, 80, "Nature Neuroscience", True)     # STRING TO SEARCH FOR

########## SHOW RESULTS #################

print "--- RESULTS --- \n"
print hitList