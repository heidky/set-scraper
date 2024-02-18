from dotenv import load_dotenv
import os
import websites.sc as sc
import websites.vg as vg
import download.downloader as dw

load_dotenv()
sc_cookie = os.getenv("SC_COOKIE")

if __name__ == '__main__':
    # url = "https://vipergirls.to/threads/5423042-Emily-Bloom-Valley-x50-6720px-(07-21-20)?highlight=emily+bloom"
    # url="https://vipergirls.to/threads/6872723-Jessica-Night-WHITE-amp-BLUE-ALL-OVER-CARD-f0993-x-50-3000-x-4500-March-16-2022?highlight=istripper"
    # thread = vg.Thread_VG(url)
    # thread.extract_sets()
    # thread.solve_sets()

    # downloader = dw.Downloader('./sets/original', 'Jni - White', thread.sets, img_sleep_secs=0.2)
    # downloader.download()

    # url = 'https://simpcity.su/threads/jessica-nigri.9946/'
    # print('hello')
    url = 'https://simpcity.su/threads/jinx-asmr.18872/'
    thread = sc.Thread_SC(url, 'Jinx', sc_cookie)
    thread.extract_sets()
    thread.solve_sets()
    print(thread.sets)
    
    downloader = dw.Downloader('./sets/original', 'Jinx', thread.sets, img_sleep_secs=0.1)
    downloader.download()
