from PIL import Image
from math import floor


def resize_to_screen(img: Image.Image, w_screen: int, h_screen: int) -> Image.Image:
    w, h = img.size
    ratio = max(w / w_screen, h / h_screen)

    if ratio <= 1:
        return img.copy()
    else:
        new_size = (round(w/ratio), round(h/ratio))
        return img.resize(new_size)
    

class Resizer:
    def __init__(self, screen_size: str | tuple[int, int]='2K'):
        if isinstance(screen_size, str):
            screen_size = screen_size.lower()

            if screen_size == '2k':
                self.w_screen = 2560
                self.h_screen = 1440
            elif screen_size == '4k':
                self.w_screen = 3840 
                self.h_screen = 2160
            elif screen_size == '1080p':
                self.w_screen = 1920
                self.h_screen = 1080
            else:
                raise ValueError("screen size as string must be one of: [1080p, 2K, 4K]")
        else:
            w, h = screen_size
            self.w_screen = round(w)
            self.h_screen = round(h)
        
    def process(self, image: Image.Image) -> Image.Image:
        return resize_to_screen(image, self.w_screen, self.h_screen)
