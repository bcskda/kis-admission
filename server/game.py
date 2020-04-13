from .utils import BaseGameServer


class GameServer(BaseGameServer):
    async def play_with_client(self, reader, writer):
        pass
