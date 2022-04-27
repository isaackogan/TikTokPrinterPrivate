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
