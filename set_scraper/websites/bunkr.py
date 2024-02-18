import re
import requests
import requests as r
import re
from bs4 import BeautifulSoup


# https://i-burger.bunkr.ru/Patreon-post-image-145418355a77b64254a-e7tVVGSR.jpg
# https://bunkr.media/i/Patreon-post-image-145418355a77b64254a-e7tVVGSR.jpg


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


class Post_Bunkr():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.headers = HEADERS

    def get_images(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        img_list = soup.select(f"div.grid-images img")

        src_list = []

        for index, img in enumerate(img_list):
            src_thumb = img.get('src')

            if src_thumb is not None:
                src = src_thumb.replace('/thumbs/', '/').replace('.png', '.jpg')
                src_list.append(src)
            else:
                print(f"skipped image with index {index}")

        return src_list