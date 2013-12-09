#HTML Parser
import BeautifulSoup
#HTTP Protocol
import urllib2
#URL Checker
from lepl.apps.rfc3696 import HttpUrl
#For time stamp
import time

def timestamp():
    #gets time since epoch
    now = time.localtime(time.time())
    #turns time from epoch into local time and parses it
    localtime = time.strftime("%H:%M:%S", now)
    #makes the final time stamp format
    return "["+ localtime +"] "
#URL is the URL to be checked
def validator(url):
    #checks for valid URL
    validator = HttpUrl()
    #returns boolean for valid URL
    return validator(url)
#p is the database to merge to, q is the source database
def union(p,q):
    #merge links with to crawl
    for e in q:
        if e not in p:
            #if link not in crawled append link too toCrawl
            p.append(e)

def spyder(SeedUrl, target):
    #DB of links to crawl in the future
    tocrawl=[SeedUrl]
    #DB of links that have been crawled
    crawled=[]
    #status message at start of crawl seed url is the first
    print timestamp() + "STARTING CRAWL WITH SEED: " + tocrawl[0]
    while tocrawl:
        page=tocrawl.pop(0)
        if validator(page) and page not in crawled:
            #print  timestamp() + page
            try:
                pagesource=urllib2.urlopen(page)
            except urllib2.HTTPError, e: #handler for HTTP exception and errors
                #Error message: Time stamp, Error code, page that caused the error 
                print timestamp() + "ERROR: " + str(e.code) + " " + page
                crawled.append(page)
            except urllib2.URLError, e: #handler for URL loading errors
                #Error message: Time Stamp, Error code, page that caused the error
                print timestamp() + "ERROR: " + str(e.code) + " " + page
                #fixes problem with loading error pages being reopened
                crawled.append(page)
            else:
                #loads the page and reads it
                s=pagesource.read()
                soup=BeautifulSoup.BeautifulSoup(s)
                #finds all links
                links=soup.findAll('a',href=True)
                if target.find("http://")== -1:
                    content = soup.findall('')
                #takes every link and takes the URL
                for index, item in enumerate(links):
                    links[index] = item['href']
                #checks if page is crawled and adds links if not in crawled... This is somewhat depreciated
                union(tocrawl,links)
                crawled.append(page)
                #debug message when page is finished being crawled
                print timestamp() + "Finished Crawl:: " + str(len(tocrawl)) + " left to crawl " 
    return crawled

spyder("""put where you want to sart crawling""","""what you URL you want to look for""")
