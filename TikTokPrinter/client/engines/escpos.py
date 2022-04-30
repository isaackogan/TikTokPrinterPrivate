import inspect
import os
from typing import Union, List, Any, Optional

import serial
import usb
from escpos.exceptions import USBNotFoundError
from escpos.printer import Usb, Serial, Network
from usb.core import NoBackendError, find

from TikTokPrinter.client.engines.console import Console
from TikTokPrinter.types.errors import MissingPrinterDriver, SetupMonkeyPatch, NoDevicesFound


class EscposEngine:
    """
    Escpos Engine for Thermal Printing

    """

    def __init__(self, engine: Union[Usb, Serial, Network, Console], **kwargs):
        """
        Initialize the EscposEngine engine class.

        :param engine: The engine you want to use for Escpos printing
        :param kwargs: Set formatting configuration for the printer

        """

        self.escpos: Union[Usb, Serial, Network, Console] = engine
        self.__process_kwargs(**kwargs)

    def __process_kwargs(self, **kwargs) -> dict:
        """
        Process kwargs into class attributes

        :param kwargs: Constructor's kwargs
        :return: Remaining values

        """

        self.align: str = kwargs.pop("align", "left")
        self.font: str = kwargs.pop("font", "a")
        self.text_type: str = kwargs.pop("text_type", "normal")
        self.width: int = kwargs.pop("width", 1)
        self.height: int = kwargs.pop("height", 1)
        self.density: int = kwargs.pop("density", 9)
        self.invert: bool = kwargs.pop("invert", False)
        self.smooth: bool = kwargs.pop("smooth", False)
        self.flip: bool = kwargs.pop("flip", False)

        return kwargs


class EscposEngineGenerator:
    """
    Static Class: Generator for the EscposEngine class

    """

    __HEADER = '\033[95m'
    __BLUE = '\033[94m'
    __CYAN = '\033[96m'
    __GREEN = '\033[92m'
    __WARNING = '\033[93m'
    __FAIL = '\033[91m'
    __RESET = '\033[0m'
    __BOLD = '\033[1m'
    __UNDERLINE = '\033[4m'
    __RED = '\033[31m'

    @staticmethod
    def __remove_printer_kwargs(**kwargs) -> dict:
        """
        Remove printer kwargs from the printer initialization

        :param kwargs: Method kwargs
        :return: Cleaned up kwargs

        """

        for key in ["align", "font", "text_type", "width", "height", "density", "invert", "smooth", "flip"]:
            try:
                del kwargs[key]
            except KeyError:
                pass

        return kwargs

    @staticmethod
    def __handle_exceptions(ex: Exception) -> None:
        """
        Handle initialization exceptions & let the client know more specifically what went wrong

        :param ex: The exception to handle
        :return: None

        """

        if isinstance(ex, NoBackendError):
            raise MissingPrinterDriver(
                "The printer system could not detect a driver. More information below:\n\n"
                "WINDOWS USERS\n\nInstall the libusK driver (or similar) via recommended Zadig installer to continue.\n"
                "Information on how to do this can be found quite easily within the setup guide for this library.\n\n"
                "MACOS USERS\n\nInstall libusb via homebrew. Your python will also need to be a homebrew install in "
                "order to recognize the libusb package when you install it via homebrew.\n\n"
                "LINUX USERS\n\n"
                "Should just be able to install libusb for Linux."
            ) from ex

        if isinstance(ex, NotImplementedError) and str(ex) == "detach_kernel_driver":
            edit_file: bool = False

            if str(os.name) == "nt":
                import escpos.printer

                fp = inspect.getsourcefile(escpos.printer)

                with open(fp, "r", encoding="utf-8") as file:
                    lines: List[str] = file.readlines()

                    if any("check_driver = None" in line for line in lines):
                        edit_file = True

                if edit_file:
                    with open(fp, "w", encoding="utf-8") as file:
                        lines = lines[:57] + lines[71:]
                        file.write("".join(lines))

            if edit_file:
                raise SetupMonkeyPatch(
                    "Your Windows-Specific setup seems to have failed. We are attempting to "
                    "retroactively fix it. Restart the script for it to take effect. "
                )

        raise ex

    @classmethod
    def __auto_select(cls, timeout: int = 1000, in_ep: hex = 0x82, out_ep: hex = 0x01, *args, **kwargs) -> EscposEngine:
        """
        Automatically select a device & input the given config

        :param timeout: Device timeout
        :param in_ep: In endpoint
        :param out_ep: Out endpoint
        :param args: create_usb args
        :param kwargs: create_usb kwargs
        :return: An EscposEngine object

        """

        # List all devices
        devices: List[Any] = list(find(find_all=True))

        # No Devices, raise error
        if len(devices) < 1:
            raise NoDevicesFound("Could not locate any USB devices on your system. Check that your device is plugged in & turned on.")

        # Enumerate through devices
        print(f"{cls.__RED}[Found {len(devices)} Total Device{'s' if len(devices) > 1 else ''}]{cls.__RESET}")
        for idx, device in enumerate(devices):
            try:
                print(
                    f"{idx + 1}. {usb.util.get_string(device, device.iProduct).strip()} ({device.manufacturer}) "
                    f"[Product ID: {hex(device.idProduct)} | Vendor ID: {hex(device.idVendor)}]"
                )
            except:
                print(
                    f"{idx + 1}. Unknown USB Device [Product ID: {hex(device.idProduct)} | Vendor ID: {hex(device.idVendor)}]"
                )

        picked: Optional[EscposEngine] = None
        _picked: Optional[Any] = None

        # Pick loop
        while not picked:
            print(f"\nInput a number from {cls.__RED}[1 to {len(devices)}]{cls.__RESET} to pick your device.")
            choice: str = input("> ")

            try:
                pick_idx = int(choice) - 1
                _picked = devices[pick_idx]

                picked = cls.create_usb(
                    vendor_id=_picked.idVendor,
                    product_id=_picked.idProduct,
                    timeout=timeout,
                    in_ep=in_ep,
                    out_ep=out_ep,
                    auto_find=False,
                    *args,
                    **kwargs,
                )

            except Exception as ex:
                print(f"\n{cls.__RED}Failed:", str(ex), f"- Try again!{cls.__RESET}")
                pass

        print(
            f"\n{cls.__GREEN}Successfully chose {usb.util.get_string(_picked, _picked.iProduct).strip()} ({_picked.manufacturer}) "
            f"[Product ID: {hex(_picked.idProduct)} | Vendor ID: {hex(_picked.idVendor)}]{cls.__RESET}\n"
        )

        return picked

    @classmethod
    def create_usb(
            cls,
            vendor_id: hex,
            product_id: hex,
            auto_find: bool = True,
            timeout: int = 1000,
            in_ep: hex = 0x82,
            out_ep: hex = 0x01,
            *args,
            **kwargs
    ) -> EscposEngine:
        """
        Initialize the EscposEngine with a USB Printer.

        To find the Vendor ID & Product ID of your printer, download USBDeview and find your device.

        For more information on kwargs, visit https://python-escpos.readthedocs.io/en/latest/.

        If you receive the Invalid Endpoint address error, pass the following in for a custom in_ep and out_ep:
        in_ep: hex = 0x81, out_ep: hex = 0x03. That *might* fix it.

        :param auto_find: Automatically detect & select from a list of USB devices
        :param vendor_id: Vendor ID of the printer
        :param product_id: Product ID of the printer
        :param timeout: Timeout for printer commands
        :param in_ep: In_ep
        :param out_ep: Out_ep
        :param args: Extra arguments
        :param kwargs: Formatting arguments & extra printer arguments
        :return: Initialized Escpos Engine with USB Printer
        :raises: MissingPrinterDriver

        """

        try:
            return EscposEngine(
                Usb(
                    idVendor=vendor_id,
                    idProduct=product_id,
                    timeout=timeout,
                    in_ep=in_ep,
                    out_ep=out_ep,
                    *args,
                    **cls.__remove_printer_kwargs(**kwargs)
                ),
                **kwargs
            )
        except Exception as ex:
            # Find printer
            if isinstance(ex, USBNotFoundError) and auto_find:
                return cls.__auto_select(timeout, in_ep, out_ep, *args, **kwargs)

            # Generic raise error
            EscposEngineGenerator.__handle_exceptions(ex)

    @classmethod
    def create_serial(
            cls,
            devfile: str = "/dev/ttyS0",
            baudrate: int = 9600,
            bytesize: int = 8,
            timeout: int = 1,
            parity: serial = serial.PARITY_NONE,
            stopbits: serial = serial.STOPBITS_ONE,
            xonxoff: bool = False,
            dsrdtr: bool = True,
            *args,
            **kwargs
    ) -> EscposEngine:
        """
        Initialize the EscposEngine with a Serial Printer.

        For more information on kwargs, visit https://python-escpos.readthedocs.io/en/latest/.

        :param devfile: devfile
        :param baudrate: baudrate
        :param bytesize: bytesize
        :param timeout: Timeout for printer commands
        :param parity: parity
        :param stopbits: stopbits
        :param xonxoff: xonxoff
        :param dsrdtr: dsrdtr
        :param args: Extra arguments
        :param kwargs: Formatting arguments & extra printer arguments
        :return: Initialized Escpos Engine with Serial Printer
        :raises: MissingPrinterDriver

        """

        try:
            return EscposEngine(
                Serial(
                    devfile=devfile,
                    baudrate=baudrate,
                    bytesize=bytesize,
                    timeout=timeout,
                    parity=parity,
                    stopbits=stopbits,
                    xonxoff=xonxoff,
                    dsrdtr=dsrdtr,
                    *args,
                    **cls.__remove_printer_kwargs(**kwargs)
                ),
                **kwargs
            )
        except Exception as ex:
            EscposEngineGenerator.__handle_exceptions(ex)

    @classmethod
    def create_network(
            cls,
            host: str,
            port: int = 9100,
            timeout: int = 60,
            *args,
            **kwargs
    ) -> EscposEngine:
        """

        For more information on kwargs, visit https://python-escpos.readthedocs.io/en/latest/.

        :param host: Hostname of the printer
        :param port: Port of the printer
        :param timeout: Printer command timeout
        :param args: Extra arguments
        :param kwargs: Formatting arguments & extra printer arguments
        :return: Initialized Escpos Engine with Network Printer
        :raises: MissingPrinterDriver
        """

        try:
            return EscposEngine(
                Network(
                    host=host,
                    port=port,
                    timeout=timeout,
                    *args,
                    **cls.__remove_printer_kwargs(**kwargs)
                ),
                **kwargs
            )
        except Exception as ex:
            EscposEngineGenerator.__handle_exceptions(ex)

    @classmethod
    def create_console(cls, **kwargs) -> EscposEngine:
        """
        Create a dummy Console printer

        :param kwargs: Mostly ignored
        :return: Initialized Escpos Engine with Console Printer

        """

        try:
            return EscposEngine(
                Console(),
                **kwargs
            )
        except Exception as ex:
            EscposEngineGenerator.__handle_exceptions(ex)
