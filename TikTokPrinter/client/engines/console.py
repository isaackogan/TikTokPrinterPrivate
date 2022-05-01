"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""

import os

from PIL import Image


class Console:
    """
    Dummy Console Printer

    """

    @classmethod
    def text(cls, txt: str):
        """
        Print text to the console

        :param txt: Text to the print
        :return: None

        """

        print(txt.rstrip(os.linesep))

    @classmethod
    def image(cls, img_source: Image):
        """
        Print an image (show image)

        :param img_source: PIL Image
        :return: None

        """

        img_source.show()

    @classmethod
    def set(cls, *args, **kwargs):
        """
        Dummy method for setting formatting- not possible in console.

        :param args: Ignored
        :param kwargs: Ignored
        :return: None

        """

        pass
