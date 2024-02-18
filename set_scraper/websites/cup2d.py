import requests
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


class Post_Cup2d():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.headers = HEADERS

    def get_images(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        img_list = soup.select(f"div.entry-content > div > a > img")
        a_list = [img.parent for img in img_list if '.jpg' in img.get('src')]

        src_list = []

        for index, a in enumerate(a_list):
            src = a.get('href')

            if src is not None:
                src_list.append(src)
            else:
                print(f"skipped image with index {index}")

        return src_list