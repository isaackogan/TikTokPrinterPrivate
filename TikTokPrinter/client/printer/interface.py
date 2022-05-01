"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""

import asyncio
import logging
import traceback
from asyncio import AbstractEventLoop, Task
from typing import Optional, List

from PIL import Image

from TikTokPrinter.client.engines.escpos import EscposEngine
from TikTokPrinter.client.printer.engine import PrinterEngine
from TikTokPrinter.types.errors import InvalidPrinterObject
from TikTokPrinter.types.objects import PrinterImage, PrinterText, PrinterCollection, VoiceText, SoundFile


class PrinterInterface:
    """
    Printer Interface, controller of everything.

    """

    QUEUE_INTERVAL: float = 0.5
    """Interval at which to handle printer messages"""

    def __init__(
            self,
            loop: AbstractEventLoop,
            engine: EscposEngine
    ):
        """
        Initialize the PrinterInterface class

        :param loop: Abstract event loop for asynchronous task handling
        :param engine: The generated EscposEngine for printing

        """

        self._engine: PrinterEngine = PrinterEngine(engine=engine, loop=loop)

        self.loop: AbstractEventLoop = loop
        self._queue: List[PrinterCollection] = list()
        self._task: Optional[Task] = None
        self.__running: bool = False

    def voice(self, content: str, index: int) -> None:
        """
        Send a voice message via the VoiceEngine

        :param content: The message (text)
        :param index: The index in the queue to insert it
        :return: None

        """

        self.queue(collection=PrinterCollection([VoiceText(content)]), index=index)

    def sound(self, file_path: str, index: int) -> None:
        """
        Play a sound file via the SoundEngine

        :param file_path: The file path of the sound to play
        :param index: The index in the queue to insert it
        :return: None

        """

        self.queue(collection=PrinterCollection([SoundFile(file_path)]), index=index)

    def text(self, content: str, index: int, bold: bool = False) -> None:
        """
        Print text to the printer via the EscposEngine

        :param content: The message to sent
        :param index: The index in the queue to insert it
        :param bold: Whether to override the bold formatting settings & make this message bold
        :return: None

        """

        lines: List[str] = content.split("\n")
        text_lines: List[PrinterText] = []

        for line in lines:
            text_lines.append(PrinterText(line, bold))

        self.queue(collection=PrinterCollection(content=text_lines), index=index)

    def image(self, content: Image, index: int) -> None:
        """
        Print an image to the printer via the EscposEngine

        :param content: The PIL Image to send
        :param index: The index in the queue to insert it
        :return: None

        """

        self.queue(collection=PrinterCollection(content=[PrinterImage(content)]), index=index)

    def queue(self, collection: PrinterCollection, index: int) -> None:
        """
        Send multiple types of messages to the engine to perform all at once, consecutively

        :param collection: The printer collection containing your desired events
        :param index: The index in the queue to insert the collection
        :return: None

        """

        # Append
        if index < 0:
            self._queue.append(collection)
            return

        # Insert
        self._queue.insert(index, collection)

    async def __printer_loop(self) -> None:
        """
        Internal printer loop for handling printer commands

        :return: None

        """

        while self.__running:
            await asyncio.sleep(self.QUEUE_INTERVAL)

            # Nothing is in the queue
            if len(self._queue) < 1:
                continue

            # Get first item in FIFO queue
            first_in: PrinterCollection = self._queue.pop(0)

            # Print the item
            try:
                await self.__print_content(collection=first_in)
            except:
                logging.error(traceback.format_exc())

    async def __print_content(self, collection: PrinterCollection) -> None:
        """
        Disseminate various engine commands to the appropriate engine

        :param collection: The collection of actions to perform
        :return: None

        """

        for item in collection.content:
            if isinstance(item, PrinterImage):
                try:
                    self._engine.image(item)
                except:
                    logging.error(traceback.format_exc())
                continue

            if isinstance(item, PrinterText):
                self._engine.text(item)
                continue

            if isinstance(item, SoundFile):
                self._engine.sound(item)
                continue

            if isinstance(item, VoiceText):
                await self._engine.voice(item)
                continue

            raise InvalidPrinterObject(f"Invalid object of type {type(item)} passed to _printer queue.")

    def start(self) -> None:
        """
        Start handling printer tasks

        :return: None

        """

        self._task = self.loop.create_task(self.__printer_loop())
        # noinspection PyProtectedMember
        self._engine._voice.start()
        self.__running = True

    def stop(self) -> None:
        """
        Stop handling printer tasks

        :return: None

        """

        self.__running = False
        self._task.cancel(msg="Stop Printer")
        # noinspection PyProtectedMember
        self._engine._voice.stop()
        self._task = None
