from asyncio import AbstractEventLoop
from typing import Optional, List

from PIL import Image, ImageOps

from TikTokPrinter.client.engines.escpos import EscposEngine
from TikTokPrinter.client.engines.sound import SoundEngine
from TikTokPrinter.client.engines.voice import VoiceEngine
from TikTokPrinter.types.errors import InvalidImageObject
from TikTokPrinter.types.objects import PrinterImage, PrinterText, VoiceText, SoundFile


class PrinterEngine:
    """
    Printer engine for sending commands to various inner engines (EscposEngine, VoiceEngine, SoundEngine, etc.)

    """

    def __init__(self, engine: EscposEngine, loop: AbstractEventLoop):
        """
        Initialize the printer engine

        :param engine: Pass in your desired Escpos engine
        :param loop: Asyncio loop

        """

        self._escpos: EscposEngine = engine
        self._voice: VoiceEngine = VoiceEngine(loop=loop)
        self._sound: SoundEngine = SoundEngine(loop=loop)

    def __set_formatting(self, bold_override: Optional[str] = None) -> None:
        """
        Internal method for updating escpos formatting with given saved values from the EscposEngine

        :param bold_override: Override the bold setting
        :return: None

        """

        text_type: str = bold_override if isinstance(bold_override, str) else self._escpos.text_type

        self._escpos.escpos.set(
            align=self._escpos.align,
            font=self._escpos.font,
            text_type=text_type,
            width=self._escpos.width,
            height=self._escpos.height,
            density=self._escpos.density,
            invert=self._escpos.invert,
            smooth=self._escpos.smooth,
            flip=self._escpos.flip
        )

    def image(self, image: PrinterImage) -> None:
        """
        Format & print an image

        :param image: Image to print
        :return: None

        """

        if not isinstance(image.content, Image.Image):
            raise InvalidImageObject(f"Provided image is invalid and is of type {type(image.content)}. Image will be skipped.")

        # Assign to variable
        content: Image = image.content

        # Escpos only flips text, we need to flip it ourselves
        if self._escpos.flip:
            content = ImageOps.flip(ImageOps.mirror(content))

        self.__set_formatting()

        # Padding 1
        if image.padding:
            self.text(PrinterText(""))

        self._escpos.escpos.image(img_source=content)
        self.text(PrinterText(""))

        # Padding 2
        if image.padding:
            self.text(PrinterText(""))

    def text(self, text: PrinterText) -> None:
        """
        Format & print text

        :param text: The text to print
        :return: None

        """

        self.__set_formatting(bold_override="B" if text.bold else None)

        content: str = text.content
        lines: List[str] = content.split("\n")

        for line in lines:
            self._escpos.escpos.text(line + "\n")

    async def voice(self, voice: VoiceText) -> None:
        """
        Format & speak a text-to-speech message

        :param voice: The text message to speak out loud
        :return: None

        """

        content: str = voice.content.replace("\n", " ")
        self._voice.speak(content)

    def sound(self, sound: SoundFile) -> None:
        """
        Play a sound

        :param sound: The sound to play
        :return: None
        """

        self._sound.play(sound.file_path)
