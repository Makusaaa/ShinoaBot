import requests
from bs4 import BeautifulSoup
from pypasser import reCaptchaV3
import json


class Anime:
  def __init__(self,title,id,episodecount):
    self.title = title
    self.id = id
    self.episodecount = episodecount

class Quality:
  def __init__(self,quality,link,size=None):
    self.quality = quality
    self.link = link
    self.size = size

class Episode:
  def __init__(self,episodenumber,title,streamlink=None,downloadlink=None,quality=None):
    self.episodenumber = episodenumber
    self.title = title
    self.streamlink = streamlink
    self.downloadlink = downloadlink
    self.quality = quality

Headers = {
    'Host': 'api.allanime.day',
    'Origin': 'https://allmanga.to'
}

def SearchAnime(keyword):
    link = 'https://api.allanime.day/api?variables={"search":{"query":"'+keyword+'"},"limit":26,"page":1,"translationType":"sub","countryOrigin":"ALL"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"06327bc10dd682e1ee7e07b6db9c16e9ad2fd56c1b769e47513128cd5c9fc77a"}}'
    anime_list = []
    result = requests.get(link, headers=Headers)
    json_result = json.loads(result.text)['data']['shows']['edges']
    for i in range(len(json_result)):
        item = json_result[i]
        title,id,= item['name'],item['_id']
        if item['availableEpisodes']['sub'] != None:
            episodecount = int(item['availableEpisodes']['sub'])
        anime_list.append(Anime(title,id,episodecount))
    return anime_list

def GetEpisodeDetail(id,ep):
    link = 'https://api.allanime.day/api?variables={"showId":"'+id+'","translationType":"sub","episodeString":"'+str(ep)+'"}&extensions={"persistedQuery":{"version":1,"sha256Hash":"5f1a64b73793cc2234a389cf3a8f93ad82de7043017dd551f38f65b89daa65e0"}}'
    result = requests.get(link, headers=Headers)
    json_result =  json.loads(result.text)
    print(result)
    if('data' not in json_result):
        return 'API Error'
    episode_data = json_result['data']['episode']
    if episode_data == None:
       return 'Episode not found!'
    title = episode_data['episodeInfo']['notes']
    stream_list = []
    for src in episode_data['sourceUrls']:
        if src['sourceUrl'].startswith('https'):
            stream_list.append(src['sourceUrl'])
        if 'downloads' in src and src['downloads']['sourceName'] == 'Gl':
            download_link = src['downloads']['downloadUrl']
    anchor = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LealdkbAAAAAHbox4XlHS8ZMQ6lkcx96WV62UfO&co=aHR0cHM6Ly9lbWJ0YWt1LnBybzo0NDM.&hl=en&v=QquE1_MNjnFHgZF4HPsEcf_2&size=invisible&cb=23w0n8ggus8d'
    reCaptcha_response = reCaptchaV3(anchor)
    quality = GetDownloadQualities(download_link,reCaptcha_response)
    return Episode(ep,title,stream_list,download_link,quality)

def GetDownloadQualities(link,captcha):
    quality_list = []
    id_download = link[link.find('?id=')+len('?id='):link.find('&title')]
    post_data = {
        'captcha_v3' : captcha,
        'id' : id_download
    }
    result = requests.post('https://embtaku.pro/download',data=post_data)
    soup = BeautifulSoup(result.text,'html.parser')
    links = soup.find_all('a')
    for item in links:
        if(item['href'][8:17] == 'gredirect'):
            quality = item.contents[0][item.contents[0].find('('):item.contents[0].find(')')].strip(' - mp4')+')'
            downloadlink = item['href']
            quality_list.append(Quality(quality,downloadlink))
    return quality_list

def FormatEpisodeDetail(episode):
    output = ''
    output += str('Ep.'+str(episode.episodenumber)+' '+episode.title+'\n')
    output += str('Stream: ')
    checkemb = False
    for links in episode.streamlink:
        if links.startswith('https://embtaku.pro/'):
            output += links+'\n'
            checkemb = True
    if checkemb == False:
        output += 'ngga ada link embtaku, adanya ini pilih aja\n'
        for links in episode.streamlink:
            output += links+'\n'
    return output
