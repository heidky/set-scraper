from dotenv import load_dotenv
import os
import sys
import websites.sc as sc
import websites.vg as vg
import websites.bunkr as bunkr
import websites.cup2d as cup2d
import download.downloader as dw
from pathlib import Path
import processing.static as ps
import yaml
import json


load_dotenv(verbose=True, override=True)
SC_COOKIE = os.getenv("SC_COOKIE") 

class SetCache:
    def __init__(self, path: Path):
        self.path = path
        self.cache_file = self.path / '.cache.json'
        self.cache_data = dict()
        
        self.__read()
      

    def __read(self):
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                self.cache_data = json.load(f)

    def __write(self):
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.cache_file, 'w') as f:
            json.dump(self.cache_data, f, indent=2)

    def get_srcs(self):
        return self.cache_data.get('srcs')
    
    def put_srcs(self, srcs):
        self.cache_data['srcs'] = srcs
        self.__write()

    def is_completed(self):
        return self.cache_data.get('completed')

    def mark_completed(self, is_compled=True):
        self.cache_data['completed'] = is_compled
        self.__write()
    

def get_post(url: str, set_name: str):
    post = None
    match url:
        case _ if '://bunkr.' in url or '://bunkrr.' in url:
            post = bunkr.Post_Bunkr(url, set_name)
        case _ if '://vipergirls.' in url:
            post = vg.Post_Vg(url, set_name)
        case _ if '://simpcity.' in url:
            post = sc.Post_Sc(url, set_name, cookie=SC_COOKIE)
        case _ if '://www.cup2d.' in url:
            post = cup2d.Post_Cup2d(url, set_name)
    return post


def scrape_post(set_name, url, path='sets/original', *, ignore=[], bypass_completed=False):

    output_path = Path('.') / path / set_name
    post = None

    cache = SetCache(output_path)

    if not bypass_completed and cache.is_completed():
        # print(">>> download already completed")
        return
    
    print(f"\n=== [{set_name}] ===")

    srcs = cache.get_srcs()
    if srcs is None:
        post = get_post(url, set_name)

        if post is None:
            raise RuntimeError("Not valid match for url:", url)
    
        srcs = post.get_images()
        cache.put_srcs(srcs)
    else:
        print('>>> set cache hit:', output_path)

    processing = [ps.Resizer('2K')]
    downloader = dw.DownloaderSimple(srcs, output_path, processing=processing, ignore=ignore)
    is_completed = downloader.download()

    if is_completed:
        print(">>> marked completed")
        cache.mark_completed()


def main():
    print("scraping...")

    if len(sys.argv) == 3 and sys.argv[1] == '-f':
        with open(sys.argv[2], 'r') as f:
            sets_file = yaml.safe_load(f)
        
        path = sets_file['path']

        for set_data in sets_file['sets']:
            name, url = set_data['name'], set_data['url']
            ignore = set_data.get('ignore')
            scrape_post(name, url, path=path, ignore=ignore)


if __name__ == '__main__':
    main()
    






# scrape_post("Jinx - Fireforce", "https://simpcity.su/threads/jinx-asmr.18872/post-79635")
# scrape_post("Jinx - Hearts", "https://simpcity.su/threads/jinx-asmr.18872/post-3442609")
# scrape_post("Octokuro - Vampire", "https://simpcity.su/threads/octokuro.9999/post-3435093")
# scrape_post("Jessica Nigri - Deer Queen", "https://simpcity.su/threads/jessica-nigri.9946/post-3290110")
# scrape_post("Emily - Valley", "https://vipergirls.to/threads/5423042-Emily-Bloom-Valley-x50-6720px-(07-21-20)?highlight=emily+bloom")
# scrape_post("Jinx - Bunkr", "https://bunkr.si/a/tA3SsEfI")
# scrape_post("Jinx - Bunkr 2", "https://bunkrr.su/a/xx7U7vrJ")
# scrape_post("Caprice - Private Show", "https://bunkrr.su/a/9GtpvaJ3")
# scrape_post("Coser_Byoru – Nyotengu Fortune Bikini", "https://www.cup2d.com/2023/09/22/coserbyoru-nyotengu-fortune-bikini/")
# scrape_post("[Bimilstory] Taeri – Vol.08 Succubus Taeri", "https://www.cup2d.com/2023/09/14/bimilstory-taeri-vol-08-succubus-taeri/")



# url = "https://vipergirls.to/threads/5423042-Emily-Bloom-Valley-x50-6720px-(07-21-20)?highlight=emily+bloom"
# url="https://vipergirls.to/threads/6872723-Jessica-Night-WHITE-amp-BLUE-ALL-OVER-CARD-f0993-x-50-3000-x-4500-March-16-2022?highlight=istripper"
# thread = vg.Thread_VG(url)
# thread.extract_sets()
# thread.solve_sets()

# downloader = dw.Downloader('./sets/original', 'Jni - White', thread.sets, img_sleep_secs=0.2)
# downloader.download()

# url = 'https://simpcity.su/threads/jessica-nigri.9946/'
# print('hello')
# url = 'https://simpcity.su/threads/jinx-asmr.18872/'
# thread = sc.Thread_SC(url, 'Jinx', sc_cookie)
# thread.extract_sets()
# thread.solve_sets()
# print(thread.sets)

# downloader = dw.Downloader('./sets/original', 'Jinx', thread.sets, img_sleep_secs=0.1)
# downloader.download()

