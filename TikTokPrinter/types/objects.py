from dataclasses import dataclass
from typing import List

from PIL import Image


class CollectionItem:
    """
    An item that can be added to a PrinterCollection and thus the printer queue

    """


@dataclass()
class PrinterCollection:
    """
    A collection of CollectionItem objects to add to the printer queue to perform various actions

    """

    content: List[CollectionItem]


@dataclass()
class PrinterImage(CollectionItem):
    """
    An image of type CollectionItem to print in the printer queue

    """

    content: Image
    padding: bool = True


@dataclass()
class PrinterText(CollectionItem):
    """
    A string of text of type CollectionItem to print in the printer queue

    """

    content: str
    bold: bool = False


@dataclass()
class VoiceText(CollectionItem):
    """
    A string of text of type CollectionItem to speak via text-to-speech in the printer queue

    """

    content: str


@dataclass()
class SoundFile(CollectionItem):
    """
    A string of text representing a file path of type CollectionItem to play in the printer queue

    """

    file_path: str
