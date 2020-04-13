import asyncio
import logging


class BaseTcpServer:
    def __init__(self, *, logger = None):
        if logger is None:
            logger = logging.getLogger(f'{__module__}.BaseTcpServer')
        self.logger_ = logger

    async def serve_forever(self, host: str, port: int):
        self.logger_.info('Server starting at %s:%d', host, port)
        tcp_server = await asyncio.start_server(self.serve_client, host, port)
        async with tcp_server:
            await tcp_server.serve_forever()
        self.logger_.info('Server finished at %s:%d', host, port)

    async def serve_client(self, reader, writer):
        raise NotImplementedError()

class BaseGameServer(BaseTcpServer):
    async def serve_client(self, reader, writer):
        peer_addr = writer.get_extra_info('peername')
        self.logger_.info('Client connect %s', peer_addr)
        try:
            await self.play_with_client(reader, writer)
        except Exception as e:
            self.logger_.info('Unhandled exception with %s: %s', peer_addr, e)
        finally:
            self.logger_.info('Client disconnect %s', peer_addr)

    async def play_with_client(self, reader, writer):
        raise NotImplementedError()
