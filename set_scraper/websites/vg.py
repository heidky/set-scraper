import re
import requests
from abc import ABC, abstractmethod
import requests as r
import re
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


# ---------------------------------------------------------------------------- #
#                                   REPLACERS                                  #
# ---------------------------------------------------------------------------- #
session = requests.Session()
session.cookies.set('nsfw_inter', '1') # used to get image from image_bam

class Replacer(ABC):
  matcher: str

  def match(self, url):
    return re.search(self.matcher, url)

  @abstractmethod
  def transform(self, url: str, a_url: str=None) -> str:
    pass 


class ViprReplacer(Replacer):
  matcher: str = r'vipr\.im/'
  
  def transform(self, url: str, a_url: str=None) -> str:
    return re.sub(r'/th/', r'/i/', url)


class ImxReplacer(Replacer):
  matcher: str = r'imx\.to/'

  def transform(self, url: str, a_url: str=None) -> str:
    url = re.sub(r'/t/', r'/i/', url)
    url = re.sub(r'/upload/small/', r'/u/i/', url)
    return url


class ImagetwistReplacer(Replacer):
  matcher: str = r'imagetwist\.im/'

  def transform(self, url: str, a_url: str=None) -> str:
    return re.sub(r'/th/', r'/i/', url)


class PixhostReplacer(Replacer):
  matcher: str = r'pixhost\.to/'

  def transform(self, url: str, a_url: str) -> str:
    url = re.sub(r'/thumbs/', r'/images/', url)
    url = re.sub(r'//t', r'//img', url)
    return url


class AcidReplacer(Replacer):
  matcher: str = r'acidimg\.cc/'

  def transform(self, url: str, a_url: str=None) -> str:
    url = re.sub('/upload/small/', '/i/', url)
    url = re.sub('//acid', '//i.acid', url)
    return url


class ImgboxReplacer(Replacer):
  matcher: str = r'imgbox\.com/'

  def transform(self, url: str, a_url: str=None) -> str:
    url = re.sub(r'_t\.', '_o.', url)
    url = re.sub('//thumbs', '//images', url)
    return url

class TurboReplacer(Replacer):
  matcher: str = r'turboimg\.net/'

  def transform(self, url: str, a_url: str=None) -> str:
    response = r.get(a_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    img = soup.select_one('#imageid')
    if not img:
      raise RuntimeError('no img', a_url)
    return img['src']

class ImageBam(Replacer):
  matcher: str = r'imagebam\.com/'

  def transform(self, url: str, a_url: str=None) -> str:
    for _ in range(2):
      response = session.get(a_url, headers=HEADERS)
      # print(response.cookies)
      # print(response.cookies)
      # with open('imagebam.html', 'wb') as f:
      #   f.write(response.content)
      # raise Error('nope')
      soup = BeautifulSoup(response.content, "html.parser")
      img = soup.select_one('.main-image')
      if img:
        return img['src']

    raise RuntimeError('no img', a_url)


replacers: list[Replacer] = [
  ViprReplacer(),
  ImxReplacer(),
  ImagetwistReplacer(),
  PixhostReplacer(),
  AcidReplacer(),
  ImgboxReplacer(),
  TurboReplacer(),
  ImageBam(),
]


class SrcSolver_VG:
    def __init__(self):
        self.headers = HEADERS
    
    def solve(self, urls):
        url, a_url = urls
        matched = [r for r in replacers if r.match(url)]

        if len(matched) == 1:
            return matched[0].transform(url, a_url)
        elif len(matched) == 0:
            raise RuntimeError(f"No match for {url}")
        else:
            raise RuntimeError(f"Duplicated matchers for {url}: {matched}")
        

class Thread_VG:
    def __init__(self, url):
        self.url = url
        self.solver = SrcSolver_VG()
        self.sets_raw = None
        self.sets = None


    def extract_sets(self):
        response = r.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        urls = []
        for a in soup.select('.content a'):
            img = a.select_one('img')
            if img:
                urls.append((img['src'], a['href']))

        self.sets_raw = { 0: urls }
        return self.sets_raw
    

    def solve_sets(self):
        res = dict()

        for set_id, set_urls_list in self.sets_raw.items():
            solved_urls_list = [self.solver.solve(set_urls) for set_urls in set_urls_list]
            res[set_id] = solved_urls_list

        self.sets = res
        return self.sets
    
    
    def extract_and_solve(self):
       self.extract_sets()
       self.solve_sets()
       return self.sets
           