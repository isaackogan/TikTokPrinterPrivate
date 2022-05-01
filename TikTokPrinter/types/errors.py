"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""


class InvalidPrinterObject(RuntimeError):
    """
    An invalid object is passed to the printer queue

    """

    pass


class InvalidImageObject(RuntimeError):
    """
    An invalid image object is passed to the printer queue.
    More than likely, if you get this, you passed an image that was of NoneType and not a Pillow image.
    To prevent this error, check your image is not None before appending it to the printer queue.

    """

    pass


class MissingPrinterDriver(RuntimeError):
    """
    You are missing a printer driver. Please install it.
    
    """

    pass


class SetupMonkeyPatch(RuntimeError):
    """
    Your Windows-specific auto-setup failed, we are monkey-patching the setup.

    """

    pass


class NoDevicesFound(RuntimeError):
    """
    No USB devices could be found connected to your system.

    """
