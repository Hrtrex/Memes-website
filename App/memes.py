#import json
#import re
import requests
from bs4 import BeautifulSoup


class Meme:
    JBZD = 'https://jbzd.com.pl/str/'
    KWEJK = 'https://kwejk.pl/top/tydzien/'
    usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }
    def __init__(self):
        self.__image = []
        self.__plus = []
        self.__title = []
        self.__descr = []
        self.__category = []
        self.__length = len(self.__image)
    #def __new__(cls):
    #    cls.get_memes_jbzd(cls)
    #def __setattr__(self):
    @property
    def image(self):
        return self.__image
    @property
    def plus(self):
        return self.__plus
    @property
    def length(self):
        if self.__length != len(self.__image):
            self.__length = len(self.__image)
        return self.__length
    #def __iter__(self):
    #def __next__(self):
        
    def get_memes_jbzd(self, page=''):
        searchurl = self.JBZD + page
        response = requests.get(searchurl, headers=self.usr_agent) # request url
        html = response.text

        # find all divs (imgs/spans) where class='article-image'
        soup = BeautifulSoup(html,'html.parser')
        images = soup.findAll('img', {'class': 'article-image'})
        pluses = soup.findAll('vote')

        for img in images:
            link = img['src'] # soup.img.attrs['src']
            self.__image.append(link)
        
        for plus in pluses:
            p = plus[':score']
            self.__plus.append(p)

    def get_memes_kwejk(self, page=''):
        searchurl = self.KWEJK + '' if page == '' else self.KWEJK + f'strona/{page}'
        response = requests.get(searchurl, headers=self.usr_agent)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # on this site in div we have both img sources and votes number
        images = soup.findAll('div', class_='media-element')

        for img in images:
            link = img['data-image']
            self.__image.append(link)

        for plus in images:
            p = plus['data-vote-up']
            self.__plus.append(p)
