from bs4 import BeautifulSoup
from flask import json
from flask.json import jsonify
import requests
import re
import logging

class WebScrapper:
    """
    WebScrapper update later
    """
    keyword_link = {}

    def __init__(self):
        pass
    
    @classmethod
    def get_html_content(cls,url):
        """
        get_html_content update later
        """
        try:
            #url = "https://en.wikipedia.org/wiki/Search_engine_optimization"
            req  = requests.get(url)
            soup = BeautifulSoup(req.text, "html.parser")
            soup = soup.find("div", {"id": "bodyContent"})
            for link in soup.find_all('a'):
                if re.match('^/wiki/[^Category:,File:,Help:,Wikipedia:,Template:,Template_talk:].*',str(link.get('href'))):
                    # clean special charset if required
                    cls.keyword_link.update({str(link.get('title')):str(link.get('href'))})
            print(json.dumps(cls.keyword_link))
        except Exception as error:
            print(str(error))


