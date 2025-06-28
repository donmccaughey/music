from pathlib import Path

from options import parse_options


def test_parse_options():
    options = parse_options(['mypath'])
    assert isinstance(options.root, Path)
    assert options.root == Path('mypath')
