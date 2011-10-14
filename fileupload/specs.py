# myapp/specs.py

from imagekit.specs import ImageSpec
from imagekit import processors

# first we define our thumbnail resize processor
class ResizeThumb(processors.Resize):
    width = 200
    height = 150
    crop = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 950


class ResizeMedium(processors.Resize):
    width = 550
    height= 400
# now let's create an adjustment processor to enhance the image at small sizes
# class EnchanceThumb(processors.Adjustment):
#     contrast = 1.2
#     sharpness = 1.1

# now we can define our thumbnail spec
class Thumbnail(ImageSpec):
    # quality = 90  # defaults to 70
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [ResizeThumb]

# and our display spec
class Display(ImageSpec):
    access_as = 'display_image'
    quality = 90  # defaults to 70
    pre_cache = True
    # increment_count = True
    processors = [ResizeDisplay]

class Medium(ImageSpec):
    # quality = 90  # defaults to 70
    access_as = 'medium_image'
    processors = [ResizeMedium]