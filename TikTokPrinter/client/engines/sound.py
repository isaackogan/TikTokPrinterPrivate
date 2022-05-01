"""
Copyright (C) Isaac Kogan, Inc - All Rights Reserved
Unauthorized copying of this project, via any medium is strictly prohibited
Proprietary work of Isaac Kogan
Written by Isaac Kogan <isaacikogan@gmail.com>, April 2022

You are permitted to use this project commercially so long as it was purchased firsthand from Isaac Kogan.
Distributing secondhand copies to others is strictly prohibited & is illegal.

You can do anything with this project except redistribute it.

"""

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
