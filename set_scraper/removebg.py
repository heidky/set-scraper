from pathlib import Path
from PIL import Image
from processing.static import resize_to_screen
from rembg import remove, new_session


if __name__ == '__main__':
    input_folder = Path('./sets/resized/Jni - White')
    output_folder = Path('./sets/rembg/Jni - White')

    input_path_list = input_folder.glob("**/*.jpg")

    for input_path in input_path_list:
        output_path = output_folder / input_path.relative_to(input_folder)
        output_path = output_path.with_suffix('.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)

        input_image = Image.open(input_path, formats=['JPEG'])
        output_image = remove(input_image, alpha_matting=True)
        output_image.save(output_path, 'PNG')
    