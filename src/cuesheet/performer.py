from dataclasses import dataclass
from typing import Optional
from .parse import to_tokens

@dataclass
class Performer:
    name: str

    @staticmethod
    def parse(performer: str) -> Optional['Performer']:
        tokens = to_tokens(performer)
        if len(tokens) < 2:
            return None

        if tokens[0].upper() != 'PERFORMER':
            return None

        del tokens[0]
        if tokens[0].startswith('"'):
            tokens[0] = tokens[0][1:]
        else:
            return None
        if tokens[-1].endswith('"'):
            tokens[-1] = tokens[-1][:-1]
        else:
            return None

        name = ' '.join([token for token in tokens if token])
        return Performer(name)
