#import json
#import re
import requests
from bs4 import BeautifulSoup

JBZD = 'https://jbzd.com.pl/top/miesiac/'
KWEJK = 'https://kwejk.pl/top/tydzien/'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}

def get_urls_jbzd(page=''):

    # url query string
    searchurl = JBZD + page

    # request url
    response = requests.get(searchurl, headers=usr_agent)
    #response = requests.get(searchurl, auth=('user', 'pass'))
    html = response.text

    # find all divs (imgs/spans) where class='article-image'
    soup = BeautifulSoup(html,'html.parser')
    images = soup.findAll('img', {'class': 'article-image'})
    pluses = soup.findAll('vote')
    
    memelinks = []
    
    for img in images:
        link = img['src'] # soup.img.attrs['src']
        memelinks.append(link)

    pluses_list = []

    for plus in pluses:
        p = plus[':score']
        pluses_list.append(p)
       

    return memelinks, pluses_list

def get_urls_kwejk(page=''):
    searchurl = KWEJK + '' if page == '' else KWEJK + f'strona/{page}'
    response = requests.get(searchurl, headers=usr_agent)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    # on this site in div we have both img sources and votes number
    images = soup.findAll('div', class_='media-element')

    memelinks = []
    for img in images:
        link = img['data-image']
        memelinks.append(link)

    pluses_list = []
    for plus in images:
        p = plus['data-vote-up']
        pluses_list.append(p)

    return memelinks, pluses_list