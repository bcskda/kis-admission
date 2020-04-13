import asyncio
import logging


ENCODING = 'utf-8'

class ValueSingleDispatch:
    def __init__(self):
        self.default_handler_ = None
        self.handlers_ = dict()

    def register(self, _key):
        def decorator(fn: callable):
            if _key in self.handlers_:
                raise KeyError(_key)
            self.handlers_[_key] = fn
            return fn

        return decorator

    def set_default(self, default: callable):
        self.default_handler_ = default

    def call(self, _key, *args, **kwargs):
        if _key in self.handlers_:
            handler = self.handlers_[_key]
        elif self.default_handler_ is not None:
            handler = functools.partial(self.default_handler_, _key)
        else:
            raise KeyError(_key)
        return handler(*args, **kwargs)

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

class StepBasedGameServer(BaseGameServer):
    async def play_with_client(self, reader, writer):
        state = await self.start_game(reader, writer)
        while not self.game_finished(state):
            await self.game_step(state)
        await self.finish_game(reader, writer, state)

    async def recv_command(self, reader) -> str:
        raw = await reader.readline()
        return raw.decode(ENCODING)

    async def send_response(self, writer, response: str):
        writer.write(response.encode(ENCODING))
        await writer.drain()

    async def game_step(self, state: dict):
        raise NotImplementedError()

    async def game_finished(self, state: dict):
        raise NotImplementedError()
