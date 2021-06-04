from bs4 import BeautifulSoup
import requests
import re
import logging

class WebScrapper:
    """
    WebScrapper update later
    """
    keywordLinkMap = {}
    MAX_KEYWORD_COUNT = 5000
    initialKeyCount = 0

    def __init__(self):
        pass
    
    @classmethod
    def updateKeywordLinkMap(cls,url):
        """
        get_html_content update later
        """
        try:
            request = requests.get(url)
            soup = BeautifulSoup(request.text, "html.parser")
            soup = soup.find("div", {"id": "bodyContent"})
            for link in soup.find_all('a'):
                if re.match('^/wiki/[^Category:,File:,Help:,Wikipedia:,Template:,Template_talk:].*',str(link.get('href'))):
                    # clean special charset if required
                    cls.keywordLinkMap.update({str(link.get('title')):str(link.get('href'))})
                    cls.initialKeyCount+=1
                    if cls.initialKeyCount >= cls.MAX_KEYWORD_COUNT:
                        break
            #remove later
            logging.info('keyword_list'+str(cls.keywordLinkMap))

        except Exception as error:
            logging.error("Error occured in WebScrapper::updateKeywordLinkMap:: Module::" +str(error))


