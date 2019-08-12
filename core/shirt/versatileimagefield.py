"""Default sizer & filter definitions."""
from __future__ import division
from __future__ import unicode_literals

from django.utils.six import BytesIO

from PIL import Image, ImageOps

from versatileimagefield.datastructures import FilteredImage, SizedImage
from versatileimagefield.registry import versatileimagefield_registry


class ZoomImage(SizedImage):
    """
    A SizedImage subclass that creates a 'cropped' image.
    See the `process_image` method for more details.
    """

    filename_key = 'zoom'
    filename_key_regex = r'zoom-c[0-9-]+__[0-9-]+'
    zoom_percentage = 1

    def get_filename_key(self):
        """Return the filename key for cropped images."""
        return "{key}-c{ppoi}".format(
            key=self.filename_key,
            ppoi=self.ppoi_as_str()
        )
        
    def zoom_on_centerpoint(self, image, width, height, ppoi=(0.5, 0.5)):
        """
        Return a PIL Image instance cropped from `image`.
        Image has an aspect ratio provided by dividing `width` / `height`),
        sized down to `width`x`height`. Any 'excess pixels' are trimmed away
        in respect to the pixel of `image` that corresponds to `ppoi` (Primary
        Point of Interest).
        `image`: A PIL Image instance
        `width`: Integer, width of the image to return (in pixels)
        `height`: Integer, height of the image to return (in pixels)
        `ppoi`: A 2-tuple of floats with values greater than 0 and less than 1
                These values are converted into a cartesian coordinate that
                signifies the 'center pixel' which the crop will center on
                (to trim the excess from the 'long side').
        Determines whether to trim away pixels from either the left/right or
        top/bottom sides by comparing the aspect ratio of `image` vs the
        aspect ratio of `width`x`height`.
        Will trim from the left/right sides if the aspect ratio of `image`
        is greater-than-or-equal-to the aspect ratio of `width`x`height`.
        Will trim from the top/bottom sides if the aspect ration of `image`
        is less-than the aspect ratio or `width`x`height`.
        Similar to Kevin Cazabon's ImageOps.fit method but uses the
        ppoi value as an absolute centerpoint (as opposed as a
        percentage to trim off the 'long sides').
        """
        
        ppoi_x_axis = int(image.size[0] * ppoi[0])
        ppoi_y_axis = int(image.size[1] * ppoi[1])
        center_pixel_coord = (ppoi_x_axis, ppoi_y_axis)
        # Calculate the aspect ratio of `image`
        orig_aspect_ratio = float(
            image.size[0]
        ) / float(
            image.size[1]
        )
        crop_aspect_ratio = float(width) / float(height)
        
        width_left = ppoi_x_axis - int((image.size[0] * self.zoom_percentage)/2)
        width_right = ppoi_x_axis + int((image.size[0] * self.zoom_percentage)/2)
        height_top = ppoi_y_axis - int((image.size[1] * self.zoom_percentage)/2)
        height_bottom = ppoi_y_axis + int((image.size[1] * self.zoom_percentage)/2)
        
        if width_left < 0:
            offset = abs(width_left)
            width_left = 0
            width_right = width_right + offset
            
        if width_right > image.size[0]:
            offset = width_right - image.size[0]
            width_right = image.size[0]
            width_left = width_left - offset
            
        if height_top < 0:
            offset = abs(height_top)
            height_top = 0
            height_bottom = height_bottom + offset
            
        if height_bottom > image.size[1]:
            offset = height_bottom - image.size[1]
            height_bottom = image.size[1]
            height_top = height_top - offset

        # Cropping the image from the original image
        return image.crop(
            (
                width_left,
                height_top,
                width_right,
                height_bottom
            )
        )
        

    def process_image(self, image, image_format, save_kwargs,
                      width, height):
        """
        Return a BytesIO instance of `image` cropped to `width` and `height`.
        Cropping will first reduce an image down to its longest side
        and then crop inwards centered on the Primary Point of Interest
        (as specified by `self.ppoi`)
        """
        imagefile = BytesIO()
        palette = image.getpalette()
        zoom_image = self.zoom_on_centerpoint(
            image,
            width,
            height,
            self.ppoi
        )
        
        zoom_image.thumbnail(
            (width, height),
            Image.ANTIALIAS
        )

        # Using ImageOps.fit on GIFs can introduce issues with their palette
        # Solution derived from: http://stackoverflow.com/a/4905209/1149774
        if image_format == 'GIF':
            zoom_image.putpalette(palette)

        zoom_image.save(
            imagefile,
            **save_kwargs
        )

        return imagefile
        
class ZoomImage75(ZoomImage):
    filename_key = 'zoom_75'
    filename_key_regex = r'zoom_75-c[0-9-]+__[0-9-]+'
    zoom_percentage = .75
    
class ZoomImage50(ZoomImage):
    filename_key = 'zoom_50'
    filename_key_regex = r'zoom_50-c[0-9-]+__[0-9-]+'
    zoom_percentage = .5
    
class ZoomImage33(ZoomImage):
    filename_key = 'zoom_33'
    filename_key_regex = r'zoom_33-c[0-9-]+__[0-9-]+'
    zoom_percentage = .33

versatileimagefield_registry.register_sizer('zoom_75', ZoomImage75)
versatileimagefield_registry.register_sizer('zoom_50', ZoomImage50)
versatileimagefield_registry.register_sizer('zoom_33', ZoomImage33)
