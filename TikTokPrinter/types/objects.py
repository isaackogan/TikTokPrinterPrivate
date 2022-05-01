"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""

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
