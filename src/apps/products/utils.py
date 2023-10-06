from copy import deepcopy

from PIL import Image


def resize_thumbnail(image, image_thumbnail) -> None:
    img_copy = deepcopy(image)
    img = Image.open(img_copy.path)

    if img.width > 200:
        new_img = (img.height, 200)
        img.thumbnail(new_img)
        img.save(img.path)
    
    image_thumbnail = img