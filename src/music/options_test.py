from pathlib import Path

from .options import Options


def test_parse():
    options = Options.parse(['mypath'])
    assert isinstance(options.root, Path)
    assert options.root == Path('mypath')
    assert not options.verbose


def test_verbose():
    options = Options.parse(['mypath', '--verbose'])
    assert isinstance(options.root, Path)
    assert options.root == Path('mypath')
    assert options.verbose
