import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time
from pathlib import Path


def get_headers(cookie=''): 
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
        # "Referer": "https://simpcity.su/threads/jessica-nigri.9946/",
        # "Sec-Ch-Ua": 'Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121',
        # "Sec-Ch-Ua-Mobile": "?0",
        # "Sec-Ch-Ua-Platform": "Windows",
        # "Sec-Fetch-Dest": "empty",
        # "Sec-Fetch-Mode": "navigate",
        # "Sec-Fetch-Site": "same-origin",
        # "Sec-Gpc": "1",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    })



class Downloader:
    def __init__(self, folder, name, sets_data, solver=None, *, img_sleep_secs=2):
        self.headers = get_headers()
        self.name = name
        self.sets_data = sets_data
        self.folder = folder
        self.solver = solver
        self.img_sleep_secs = img_sleep_secs


    def download(self):
        root_path = Path(self.folder) / self.name

        for set_index, (set_id, set_img_urls) in enumerate(self.sets_data.items()):
            if len(set_img_urls) > 1:
                print('>SET: downloading set:', set_index)
                set_path = root_path / f's{set_index}'
                set_path.mkdir(parents=True, exist_ok=True)

                for img_index, img_url in enumerate(set_img_urls):
                    try:
                        img_path = set_path / f"i{img_index}.jpg"

                        if not img_path.exists():
                            print('\t>IMG: downloading img:', img_index)

                            if self.solver:
                                img_src = self.solver.solve(img_url)
                            else:
                                img_src = img_url

                            self._download_image_simple(img_src, img_path)
                            time.sleep(self.img_sleep_secs)
                    except:
                        print("\tIMG: failed download:", img_url)
            else:
                print('xSET: skipping set (too small):', set_index)


    def _download_image_simple(self, src, path):
        if src is None:
            print('\tDWN: skipping image path:', path)
            return
        
        response = requests.get(src, headers=self.headers)
        if response.status_code != 200:
            print("\tDWN: src download failed", response.status_code, src)
        
        with open(path, 'wb') as handler:
            handler.write(response.content)

