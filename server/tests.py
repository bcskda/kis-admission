import asyncio
import logging
import pytest
import threading
import time
from .game import GameServer
from .utils import ENCODING
from .__main__ import run_game_server


SERVER = ('127.0.0.1', 1337)

def setup_module():
    def start_server():
        logger = logging.getLogger('GameServerDebug')
        logger.setLevel(logging.DEBUG)
        asyncio.run(run_game_server([SERVER[0]], SERVER[1], logger))

    threading.Thread(target=start_server).start()
    time.sleep(2)

def teardown_module():
    pass

def test_hello():
    async def routine():
        reader, writer = await asyncio.open_connection(*SERVER)
        # Get intro:
        lines = [await reader.readline() for line in range(5)]
        lines = map(lambda b: b.decode(ENCODING), lines)
        assert ''.join(lines) == '''Hello, peer!
            You have 5 tries to guess the word.
            Type in letters.
            Type ? to view game state.
            Good luck!
            '''

    asyncio.run(routine())
