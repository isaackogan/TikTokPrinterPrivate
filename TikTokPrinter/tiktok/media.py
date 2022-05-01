"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""

import io
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter
from TikTokLive.types import Gift, User

from TikTokPrinter.tiktok.http import GiftImage, ProfileImage


class TikTokMedia:
    """
    TikTokMedia formatting class providing utilities to format various media

    """

    @classmethod
    async def gift_image(cls, gift: Gift, size: int = 200) -> Image:
        """
        Download a gift image

        :param gift: The gift object
        :param size: The size to return the image as
        :return: The gift image

        """

        try:
            profile: GiftImage = GiftImage(gift)
            im_bytes: bytes = await profile.to_bytes()

            buffer: io.BytesIO = io.BytesIO(im_bytes)
            buffer.seek(0)

            im_pil: Image = Image.open(buffer)
        except:
            return None

        return im_pil.resize((size, size))

    @classmethod
    async def user_image(
            cls,
            user: User,
            size: int = 200,
            circle: bool = True,
            circle_blur_radius: int = 3
    ) -> Image:
        """
        Download a user's profile image

        :param user: The user to download the image for
        :param size: The size to return the image as
        :param circle: Whether to crop the image into a circle
        :param circle_blur_radius: If cropping into a circle, add an optional blur around the crop area (looks nicer)
        :return: The user's profile image

        """

        async def download(index: int):
            try:
                profile: ProfileImage = ProfileImage(user, index=index)
                im_bytes: bytes = await profile.to_bytes()

                buffer: io.BytesIO = io.BytesIO(im_bytes)
                buffer.seek(0)
                return Image.open(buffer)

            except:
                return None

        # Make three attempts
        im_pil: Optional[Image] = None
        for x in range(3):
            im_pil = await download(x)

            if im_pil is not None:
                break

        # If invalid, return
        if im_pil is None:
            return None

        # Resize
        im_pil = im_pil.resize((size, size))
        return im_pil if not circle else cls.mask_circle_transparent(im_pil, circle_blur_radius)

    @classmethod
    def mask_circle_transparent(cls, original: Image, blur_radius: int, offset: int = 0) -> Image:
        """
        Crop image into circle with a transparent background
        Via https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/

        :param original: Image to crop
        :param blur_radius: Radius for blur (intensity)
        :param offset: Image offset
        :return: New Image

        """

        offset += blur_radius * 2
        mask = Image.new("L", original.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, original.size[0] - offset, original.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = original.copy()
        result.putalpha(mask)

        return result

    @classmethod
    def remove_transparency(cls, image: Image, background: Tuple[int, int, int] = (255, 255, 255)) -> Image:
        """
        Remove transparency from an RGBA image

        :param image: The image to remove transparency from
        :param background: The colour for the new background
        :return: The transformed image

        """

        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            alpha = image.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", image.size, background + (255,))
            bg.paste(image, mask=alpha)
            return bg

        else:
            return image
