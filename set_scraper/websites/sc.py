import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time
from pathlib import Path


def get_headers(cookie): 
    return ({
        # ":authority": "simpcity.su",
        # ":method": "GET",
        # ":path": "/threads/jessica-nigri.9946/page-29",
        # ":scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        # "Cache-Control": "max-age=0",
        "Cookie": cookie,
        # "If-Modified-Since": "Sat, 03 Feb 2024 16:01:22 GMT",
        "Referer": "https://simpcity.su/threads/jessica-nigri.9946/",
        "Sec-Ch-Ua": 'Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    })


class SrcSolver_SC_Fast:
    def solve(self, url):
        return url.replace('.md.', '.')


class SrcSolver_SC:
    def __init__(self):
        self.headers = get_headers('')

    def solve(self, url):
        response = requests.get(url, headers=self.headers)
        status = response.status_code
        if status != 200:
            print("invalid jpg page", response.status_code, url)
            if status == 403 or status == 404:
                return None

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.select_one("#image-viewer-container > img")
        img_src = img_tag.get('src').replace('.md.', '.')
        return img_src


class Thread_SC:
    def  __init__(self, url, name, cookie, *, page_sleep_secs=2, verbose=False):
        self.url = url
        self.name = name
        self.headers = get_headers(cookie)
        self.page_sleep_secs = page_sleep_secs
        self.sets_raw = None
        self.sets = None
        self.solver = SrcSolver_SC_Fast()
    

    def extract_sets(self):
        # dict: int -> list[img_links], int equals hash of tuple[img_links]
        all_sets = dict()

        # TODO: cache this
        pages_text = self._download_pages_text()

        for pt in pages_text:
            set_data = self._parse_sets_from_page(pt)
            all_sets.update(set_data)

        self.sets_raw = all_sets
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
    
    
    def _download_num_pages(self, soup):
        page_nav = soup.select('ul.pageNav-main > li.pageNav-page > a')
        num = -1

        for pn in page_nav:
            try:
                n = int(pn.text)
                num = max(num, n)
            except:
                pass

        return num


    def _download_pages_text(self):
        pages_text = []
        
        response1 = requests.get(self.url + f"page-{1}", headers=self.headers)
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        num_pages = self._download_num_pages(soup1)

        for i in range(1, num_pages + 1):
            url = self.url + f"page-{i}"
            print(f"extracting: {url}")

            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(response.status_code)
                break
            else:
                # print(response.text)
                # print()
                # print()
                pass

            pages_text.append(response.text)
            time.sleep(self.page_sleep_secs)

        return pages_text
    

    def _parse_sets_from_page(self, page_text):
        soup = BeautifulSoup(page_text, "html.parser")
        img_list = soup.find_all("img")
        imgs = set()
        for i in img_list:
            a = i.parent
            div_check = a.parent
            a_href = a.get('href')
            if(a_href and div_check.name == 'div'):
                # print(a_href)
                if('jpg' in a_href):
                    imgs.add(i)

        sets = defaultdict(lambda: list())

        for i in imgs:
            src = i.get('src')
            article = i.parent.parent.parent
            sets[article].append(src)
        
        sets_serializable = dict()
        
        for k, v in sets.items():
            set_id = hash(tuple(v))
            sets_serializable[set_id] = v

        # for k,v in sets_serializable.items():
        #     print(k, v)
        #     print()

        return sets_serializable
    



class Post_Sc():
    def __init__(self, url, name, *, cookie):
        self.url = url
        self.name = name
        self.headers = get_headers(cookie)

    def get_images(self):
        post_id = self.url.split("/")[-1]

        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.select_one(f"article#js-{post_id}")

        if article is None:
            print(response.text)
        # img_list = article.select("article.message-body img")
        img_list = article.select("div.bbWrapper img")

        src_list = []

        for index, img in enumerate(img_list):
            src = img.get('src')

            if src is not None:
                src = src.replace('.md.', '.')
                src_list.append(src)
            else:
                print(f"skipped image with index {index}")

        return src_list