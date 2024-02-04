from dotenv import load_dotenv
import os
import websites.sc as sc
import websites.vg as vg
import download.downloader as dw

load_dotenv()
sc_cookie = os.getenv("SC_COOKIE")

if __name__ == '__main__':
    url = "https://vipergirls.to/threads/5423042-Emily-Bloom-Valley-x50-6720px-(07-21-20)?highlight=emily+bloom"
    thread = vg.Thread_VG(url)
    thread.extract_sets()
    thread.solve_sets()

    downloader = dw.Downloader('./sets/original', 'EB - Fairy', thread.sets, img_sleep_secs=0.2)
    downloader.download()

    # url = 'https://simpcity.su/threads/jessica-nigri.9946/'
    # thread = sc.Thread_SC(url, 'JN', sc_cookie)
    # thread.extract_sets()
    # thread.solve_sets()
    
    # downloader = dw.Downloader('./sets', 'JN', thread.sets, img_sleep_secs=0.1)
    # downloader.download()
