import requests
from bs4 import BeautifulSoup as bs

def GetLink(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    iframe = bs(requests.get(url,headers=headers).text,'html.parser').find('iframe')['src']

    headers['Referer'] = url
    getvidlink = requests.get(iframe,headers=headers).text
    getvidlink = getvidlink[getvidlink.find('$.getJSON("')+len('$.getJSON("'):]
    getvidlink = 'https://embed.watchanimesub.net'+getvidlink[:getvidlink.find('"')]

    headers['Referer'] = iframe
    headers['X-Requested-With'] = 'XMLHttpRequest'
    result = requests.get(getvidlink, headers=headers).json()

    return result['server']+'/getvid?evid=' + result['enc']

def GetAllLinks(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
    try:
        page = bs(requests.get(url,headers=headers).text,'html.parser')
        title = (page.find('h1').find('a').contents[0]).replace(' ','-')
        videos = page.find_all('a',class_='sonra')
    except:
        return 'Not Link'

    if len(videos) == 0:
        return None
    return videos[::-1]