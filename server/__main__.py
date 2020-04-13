import argparse
import asyncio
from typing import List
from .game import GameServer


async def run_server(hosts: List[str], port: int):
    log_prefix = 'GameServer'
    server = GameServer(logger=logging.getLogger(log_prefix))
    serve_coros = map(lambda host: server.serve_forever(host, port),
                      hosts)
    done, pending = asyncio.wait(serve_coros)
    assert not pending

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, default='127.0.0.1')
    parser.add_argument('port', type=int)
    args = parser.parse_arguments()
    asyncio.run(run_server(args.hosts, args.port))

if __name__ == '__main__':
    main()
