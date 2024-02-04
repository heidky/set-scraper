from PIL import Image
from math import floor

def resize_to_screen(img: Image.Image, w_screen: int, h_screen: int):
    w, h = img.size
    ratio = max(w / w_screen, h / h_screen)

    if ratio <= 1:
        return img.copy()
    else:
        new_size = (floor(w/ratio), floor(h/ratio))
        return img.resize(new_size)