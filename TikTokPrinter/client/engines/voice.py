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
from threading import Thread
from typing import Optional, List

import pyttsx3


def _speak(*args) -> None:
    """
    Speak a message (meant for internal library use only)

    :param args: What to say
    :return: None

    """

    engine = pyttsx3.init()
    engine.say(args[0])
    engine.runAndWait()


class VoiceEngine:
    """
    VoiceEngine for text-to-speech

    """

    QUEUE_INTERVAL: float = 0.1
    """How long to wait between voice messages"""

    def __init__(self, loop: AbstractEventLoop):
        """
        Initialize the VoiceEngine class

        :param loop: Asyncio event loop for creating asynchronous tasks

        """

        self.loop: AbstractEventLoop = loop
        self._queue: List[str] = list()
        self._task: Optional[Task] = None
        self.__running: bool = False

    def speak(self, text: str) -> None:
        """
        Speak a text message with a given string

        :param text: The utterance to speak
        :return: None

        """

        self._queue.append(text)

    async def __speak_loop(self) -> None:
        """
        The loop for checking against the queue & running text-to-speech

        :return: None

        """

        thread: Optional[Thread] = None

        while self.__running:
            await asyncio.sleep(self.QUEUE_INTERVAL)

            # Nothing is in the queue
            if len(self._queue) < 1:
                continue

            try:
                # Thread exists & is running, wait for it to finish
                if isinstance(thread, Thread) and thread.is_alive():
                    continue

                # Start a thread & run TTS within it
                thread: Thread = Thread(target=_speak, args=(self._queue.pop(0),))
                thread.start()

            except:
                logging.error(traceback.format_exc())

    def start(self) -> None:
        """
        Start the voice engine's queue loop

        :return: None

        """
        self._task = self.loop.create_task(self.__speak_loop())
        self.__running = True

    def stop(self) -> None:
        """
        Stop the voice engine's queue loop

        :return: None

        """
        self.__running = False
        self._task.cancel(msg="Stop Printer")
        self._task = None
