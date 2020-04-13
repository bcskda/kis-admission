import argparse
import asyncio
from typing import List
from .game import GameServer


MAX_GUESSES = 5
LOG_PREFIX = 'GameServer'

async def run_game_server(hosts: List[str], port: int, logger):
    server = GameServer(max_guessed=MAX_GUESSES, magic_word='blob', logger=logger)
    serve_coros = map(lambda host: server.serve_forever(host, port),
                      hosts)
    done, pending = asyncio.wait(serve_coros)
    assert not pending

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('-v', action='store_true', type=bool, default=False)
    args = parser.parse_arguments()

    logger = logging.getLogger(LOG_PREFIX)
    if args.v:
        logger.setLevel(logging.INFO)
    asyncio.run(run_game_server([args.host], args.port, logger))

if __name__ == '__main__':
    main()
