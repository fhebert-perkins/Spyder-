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
    startTime = time.localtime()
    seqNum = 0
    #DB of links to crawl in the future
    tocrawl=[SeedUrl]
    #DB of links that have been crawled
    crawled=[]
    #status message at start of crawl seed url is the first
    print timestamp() + "STARTING CRAWL WITH SEED: " + tocrawl[0]
    while tocrawl:
        page=tocrawl.pop(0)
        #Ghetto fixes for common errors...
        if validator(page) and page not in crawled and page.find(".pdf") == -1:
            #Uncomment the line below for Url Debugging useful for finding which website is at fault for the errors you are having
            #print  timestamp() + page
            try:
                pagesource=urllib2.urlopen(page)
            except urllib2.HTTPError, e: #handler for HTTP exception and errors
                #Error message: Time stamp, Error code, page that caused the error 
                print timestamp() + "ERROR: " + str(e.code) + " " + page
                crawled.append(page)
            except urllib2.URLError, e: #handler for URL loading errors
                #Error message: Time Stamp, Error code, page that caused the error
                print timestamp() + "ERROR: " + str(e) + " " + page
                #fixes problem with loading error pages being reopened
                crawled.append(page)
            else:
                Extension = "/"
                domain = ''
                urldomain0 = page.split('/')
                domain = urldomain0.pop(2)
                #loads the page and reads it
                s=pagesource.read()
                soup=BeautifulSoup.BeautifulSoup(s)
                #finds all links
                links=soup.findAll('a',href=True)
                if target.find("http://")== -1:
                    pass
                    #content = soup.findall('')
                #takes every link and takes the URL to scrape
                for index, item in enumerate(links):
                    links[index] = item['href']
                #checks if page is crawled and adds links if not in crawled... This is somewhat depreciated
                union(tocrawl,links)
                crawled.append(page)
                seqNum = seqNum + 1
                #debug message when page is finished being crawled
                print timestamp() + "Finished Crawl:: " + str(len(tocrawl)) + " left to crawl " + " Crawled " + str(seqNum) + " pages " + domain
                #output for seq number
    endTime = time.localtime()

    return crawled, endTime-startTime

spyder('http://google.com','hi')
