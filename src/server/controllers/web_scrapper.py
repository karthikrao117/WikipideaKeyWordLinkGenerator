from bs4 import BeautifulSoup
from collections import deque
from .mongo_db_access import DBConnection
import requests
import re
import logging
import threading

lock = threading.Lock()


class WebScrapper:
    """
    WebScrapper update later
    """
    keywordLinkMap = {}
    MAX_KEYWORD_COUNT = 5000
    initialKeyCount = 0
    
    Queue = deque()
    wikiPediaPrefix = "https://en.wikipedia.org"
    def __init__(self):
        pass
    
    @staticmethod
    def clean_url(urlvalue):
        """
        """
        return str(urlvalue).lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".","_")

    @classmethod
    def get_html_content(cls, url):
        """
        get_html_content update later
        """
        try:
            request = requests.get(url)
            if request.status_code == 200:
                if DBConnection.wiki_link_exists(WebScrapper.clean_url(url.split('/')[-1])):
                    return True
                cls.get_wiki_links(request)
                # remove later
                #logging.info('keyword_list'+str(cls.keywordLinkMap))
                DBConnection.db_update_collection_data(WebScrapper.clean_url(url.split('/')[-1]),cls.keywordLinkMap)
                while cls.initialKeyCount <= cls.MAX_KEYWORD_COUNT and cls.Queue:
                    cls.keywordLinkMap = {}
                    cls.get_html_content(cls.wikiPediaPrefix+str(cls.Queue.popleft()))
                return True
            return False
        except Exception as error:
            logging.error(
                "Error occured in WebScrapper::get_html_content:: Module::" + str(error))
            return "Exception Ocuured"

    @classmethod
    def get_wiki_links(cls, request):
        try:
            soup = BeautifulSoup(request.text, "html.parser")
            soup = soup.find("div", {"id": "bodyContent"})
            for link in soup.find_all('a'):
                if re.match('^/wiki/[^Category:,File:,Help:,Wikipedia:,Template:,Template_talk:].*', str(link.get('href'))):
                    keyword = WebScrapper.clean_url(link.get('title'))
                    cls.keywordLinkMap.update({keyword: str(link.get('href'))})
                    cls.Queue.append(str(link.get('href')))
                    cls.initialKeyCount += 1
                    logging.warning(cls.initialKeyCount)
                    if cls.initialKeyCount >= cls.MAX_KEYWORD_COUNT:
                        
                        break
        except Exception as error:
            logging.error(
                "Error occured in WebScrapper::get_html_content:: Module::" + str(error))
            return "Exception Ocuured"






