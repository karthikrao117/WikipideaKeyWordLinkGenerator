from bs4 import BeautifulSoup
from collections import deque

from .mongo_service_model import DBConnection

import requests
import re
import logging

class WebScrapper:
    """
    WebScrapper update later
    """
    keyword_linkmap = {}
    MAX_KEYWORD_COUNT = 5000
    initialkey_count = 0
    Queue = deque()
    wikipedia_prefix = "https://en.wikipedia.org"

    def __init__(self):
        pass
    
    @staticmethod
    def clean_string(urlvalue):
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
                if DBConnection.wiki_link_exists(WebScrapper.clean_string(url.split('/')[-1])):
                    return True
                cls.get_wiki_links(request)
                DBConnection.db_update_collection_data(WebScrapper.clean_string(url.split('/')[-1]),cls.keyword_linkmap)
                while cls.initialkey_count <= cls.MAX_KEYWORD_COUNT and cls.Queue:
                    cls.keyword_linkmap = {}
                    cls.get_html_content(cls.wikipedia_prefix+str(cls.Queue.popleft()))
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
                    keyword = WebScrapper.clean_string(link.get('title'))
                    cls.keyword_linkmap.update({keyword: str(link.get('href'))})
                    cls.Queue.append(str(link.get('href')))
                    cls.initialkey_count += 1
                    logging.warning(cls.initialkey_count)
                    if cls.initialkey_count >= cls.MAX_KEYWORD_COUNT:
                        break
        except Exception as error:
            logging.error(
                "Error occured in WebScrapper::get_wiki_links:: Module::" + str(error))
            return "Exception Ocuured"

    @classmethod
    def get_keyword_wikilinks(cls, search_key):
        """
        """
        output_list =[]
        try:
            search_key = WebScrapper.clean_string(search_key)
            output_list = DBConnection.get_wiki_link_list(search_key)
            if output_list:
                return output_list
            else:
                return False
        except Exception as error:
            logging.error(
                "Error occured in WebScrapper::get_keyword_wikilinks:: Module::" + str(error))
            return "Exception Ocuured"



