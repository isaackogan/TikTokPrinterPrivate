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
