from pathlib import Path
from PIL import Image
from processing.static import resize_to_screen


if __name__ == '__main__':
    input_folder = Path('./sets/original/JN')
    output_folder = Path('./sets/resized/JN')

    input_path_list = input_folder.glob("**/*.jpg")

    for input_path in input_path_list:
        output_path = output_folder / input_path.relative_to(input_folder)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            input_image = Image.open(input_path)
            output_image = resize_to_screen(input_image, 2560, 1440)
            output_image.save(output_path, 'JPEG')
        except:
            print("xSKIP:", input_path)
    