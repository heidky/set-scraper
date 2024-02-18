from dotenv import load_dotenv
import os
import websites.sc as sc
import websites.vg as vg
import websites.bunkr as bunkr
import download.downloader as dw
from pathlib import Path
import processing.static as ps

load_dotenv()
sc_cookie = os.getenv("SC_COOKIE")


def scrape_post(set_name, url):
    output_path = Path('./sets/original') / set_name
    post = None

    match url:
        case _ if '://bunkr.' in url or '://bunkrr.' in url:
            post = bunkr.Post_Bunkr(url, set_name)
        case _ if '://vipergirls.' in url:
            post = vg.Post_Vg(url, set_name)
        case _ if '://simpcity.' in url:
            post = sc.Post_Sc(url, set_name, cookie=sc_cookie)

    if post is None:
        raise RuntimeError("Not valid match for url:", url)
    
    images = post.get_images()

    processing = [ps.Resizer('2K')]
    downloader = dw.DownloaderSimple(images, output_path, processing=processing)
    downloader.download()


if __name__ == '__main__':
    # scrape_post("Jinx - Fireforce", "https://simpcity.su/threads/jinx-asmr.18872/post-79635")
    # scrape_post("Jinx - Hearts", "https://simpcity.su/threads/jinx-asmr.18872/post-3442609")
    # scrape_post("Octokuro - Vampire", "https://simpcity.su/threads/octokuro.9999/post-3435093")
    # scrape_post("Jessica Nigri - Deer Queen", "https://simpcity.su/threads/jessica-nigri.9946/post-3290110")
    scrape_post("Emily - Valley", "https://vipergirls.to/threads/5423042-Emily-Bloom-Valley-x50-6720px-(07-21-20)?highlight=emily+bloom")
    # scrape_post("Jinx - Bunkr", "https://bunkr.si/a/tA3SsEfI")
    # scrape_post("Jinx - Bunkr 2", "https://bunkrr.su/a/xx7U7vrJ")
    # scrape_post("Caprice - Private Show", "https://bunkrr.su/a/9GtpvaJ3")










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

