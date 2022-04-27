import functools
import os.path
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from typing import Awaitable

from playsound import playsound


class SoundEngine:
    """
    Sound engine for playing sounds

    """

    def __init__(self, loop: AbstractEventLoop):
        """
        Initialize the SoundEngine class

        :param loop: Asyncio event-loop for threading sound-playing tasks

        """
        self.loop: AbstractEventLoop = loop

    def play(self, file_path: str) -> Awaitable:
        """
        Play a song at a given file path

        :param file_path: Path to play file
        :return: None

        """

        if not os.path.exists(file_path):
            raise FileNotFoundError("Could not find the requested sound file")

        return self.loop.run_in_executor(ThreadPoolExecutor(), functools.partial(playsound, file_path))
