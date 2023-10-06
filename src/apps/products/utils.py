from io import BytesIO
from PIL import Image
import os

from django.core.files.base import ContentFile

from src.settings import MAX_THUMBNAIL_WIDTH


def make_thumbnail(model):
    image = Image.open(model.product_image)
    size=model.product_image.height, MAX_THUMBNAIL_WIDTH
    image.thumbnail(size)

    thumb_name, thumb_extension = os.path.splitext(model.product_image.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = thumb_name + '_thumb' + thumb_extension

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False   # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
    model.product_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()

    return True