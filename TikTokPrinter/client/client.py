from typing import Optional

from PIL import Image
from TikTokLive import TikTokLiveClient

from .engines.escpos import EscposEngine
from .printer import PrinterInterface
from ..types.objects import PrinterCollection


class TikTokPrinterClient(TikTokLiveClient):
    """
    The TikTokPrinterClient. This is the main class users interact with
    when they want to do anything with this project.

    """

    def __init__(
            self,
            unique_id: str,
            engine: EscposEngine,
            **options
    ):
        """
        Initialize the TikTokPrinterClient class

        :param unique_id: The username of the user to connect to
        :param engine: The engine to use when connecting
        :param options: Various configuration options to pass to the underlying TikTokLiveClient

        """

        options["process_initial_data"] = False
        super().__init__(unique_id, **options)

        # The printer interface
        self._printer: PrinterInterface = PrinterInterface(
            loop=self.loop,
            engine=engine
        )

    def voice(self, content: str, index: int = -1) -> None:
        """
        Send a voice message via the VoiceEngine

        :param content: The message (text)
        :param index: The index in the queue to insert it
        :return: None

        """

        self._printer.voice(content=content, index=index)

    def text(self, content: str, bold: bool = False, index: int = -1) -> None:
        """
        Print text to the printer via the EscposEngine

        :param content: The message to sent
        :param index: The index in the queue to insert it
        :param bold: Whether to override the bold formatting settings & make this message bold
        :return: None

        """

        self._printer.text(content=content, bold=bold, index=index)

    def image(self, content: Image, index: int = -1) -> None:
        """
        Print an image to the printer via the EscposEngine

        :param content: The PIL Image to send
        :param index: The index in the queue to insert it
        :return: None

        """

        self._printer.image(content=content, index=index)

    async def sound(self, file_path: str, index: int = -1) -> None:
        """
        Play a sound file via the SoundEngine

        :param file_path: The file path of the sound to play
        :param index: The index in the queue to insert it
        :return: None

        """

        self._printer.sound(file_path=file_path, index=index)

    def queue(self, *commands, index: int = -1) -> None:
        """
        Send multiple types of messages to the engine to perform all at once, consecutively

        :param commands: A list of the commands to queue in a single collection
        :param index: The index in the queue to insert the collection of commands
        :return: None

        """

        self._printer.queue(collection=PrinterCollection(list(commands)), index=index)

    async def start(self, session_id: Optional[str] = None) -> Optional[str]:
        """
        Start the printer interface & underlying engines ASYNCHRONOUSLY, without blocking the main thread.

        :param session_id: Optional session ID to connect with
        :return: None

        """

        room_id: Optional[str] = await super(TikTokPrinterClient, self).start(session_id=session_id)
        self._printer.start()
        return room_id

    def run(self, session_id: Optional[str] = None) -> None:
        """
        Start the printer interface & underlying engines SYNCHRONOUSLY, blocking the main thread.

        :param session_id: Optional session ID to connect with
        :return: None

        """

        self._printer.start()
        super(TikTokPrinterClient, self).run()
