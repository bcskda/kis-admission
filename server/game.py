import string
from .utils import StepBasedGameServer, ValueSingleDispatch


class GameServer(StepBasedGameServer):
    REPEAT_FMT = '''--- {message}
    Game state:
    Word: {word}
    Letters tried: {letters}
    Tries left: {tries_left}
    '''

    HELP_FMT = '''Hello, {peer}!
        You have {tries} tries to guess the word.
        Type in letters.
        Type ? to view game state.
        Good luck!
        '''

    ASCII = set(string.ascii_lowercase)

    def __init__(self, *args, *, max_guesses: int, magic_word: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_guesses = max_guesses
        self.magic_word = magic_word

    command_dispatcher = ValueSingleDispatch()

    async def start_game(self, reader, writer):
        initial_state = {
            'word': await self.makeup_word(),
            'tried_letters': set(),
            'guessed': False,
        }
        self.send_help()
        self.send_response(self.mask(initial_state) + '\n')
        return initial_state

    async def finish_game(self, reader, writer, state: dict):
        if state['guessed']:
            self.send_response('Congratulations!')
        else:
            self.send_response('Word: {0}'.format(state['word']))

    def game_finished(self, state: dict) -> bool:
        tries = len(state['tried_letters'])
        return state['guessed'] or tries >= self.max_tries

    async def game_step(self, reader, writer, state: dict):
        command = await self.recv_command(reader)
        response = command_dispatcher(command, word, tried_letters)
        await self.send_response(writer, response)

    @command_dispatcher.register('?')
    def on_repeat(self, state: dict) -> str:
        return self.make_info_message(state, '')

    @command_dispatcher.set_default
    def on_letter(self, letter: str, state: dict) -> str:
        letter = self.validate(letter)
        if letter in state['tried_letters']:
            masked = self.mask(word, tried_letters)
            headline = '"{0}" already known to be invalid'.format(letter)
            response = self.make_info_message(state, headline)
        else:
            state['tried_letters'].add(letter)
            response = self.mask(state['word'], state['tried_letters'])
            if '*' not in response:
                state['guessed'] = True
        return response

    async def send_help(self, writer):
        peer_addr = writer.get_extra_info('peername')
        intro = self.HELP_FMT.format(peer=peer_addr, tries=self.max_tries)
        self.send_response(intro)

    def make_info_message(self, state: dict, headline: str):
        masked = self.mask(state['word'], state['tried_`letters'])
        return self.REPEAT_FMT.format(
            headline=headline,
            word=masked, letters=state['tried_letters'],
            tries_left=self.max_tries - len(state['tried_letters']))

    async def makeup_word(self) -> str:
        self.logger_.warning('TODO implement GameServer.makeup_word()')
        return self.magic_word

    def mask(self, state: dict) -> str:
        masked = state['word']
        for letter in self.ASCIILOWER - state['tried_letters']:
            masked = masked.replace(letter, '*')
        return masked

    def validate_letter(self, letter: str):
        assert len(letter) == 1
        letter = letter.lower()
        assert letter in self.ASCIILOWER
        return letter
