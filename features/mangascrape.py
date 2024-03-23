import requests

class Manga:
  def __init__(self,title,titlelink,totalchapter=None):
    self.title = title
    self.titlelink = titlelink
    self.totalchapter = totalchapter

def SearchManga(keyword):
    mangalist = requests.post('https://manga4life.com/_search.php').json()
    result = []
    for x in mangalist:
        if keyword.lower() in x['s'].lower(): result.append(Manga(x['s'],x['i']))
    return result

def GetTotalChapter(name):
    link = 'https://www.manga4life.com/manga/'+name
    manga_page = requests.get(link).text
    a = manga_page.find('vm.Chapters = [{"Chapter":"')+len('vm.Chapters = [{"Chapter":"')+1
    b = manga_page[a:].find('"')+a-1
    return int(manga_page[a:b])