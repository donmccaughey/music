from pathlib import Path

from .options import Options


def test_parse():
    options = Options.parse(['mypath'])

    assert isinstance(options.root, Path)
    assert options.root.is_absolute()
    assert options.root.name == 'mypath'

    assert not options.verbose


def test_parse_expands_tilde():
    options = Options.parse(['~/mypath'])

    assert isinstance(options.root, Path)
    assert options.root.is_absolute()
    assert options.root.name == 'mypath'
    assert options.root.parent.name != '~'

    assert not options.verbose


def test_verbose():
    options = Options.parse(['mypath', '--verbose'])

    assert isinstance(options.root, Path)
    assert options.root.is_absolute()
    assert options.root.name == 'mypath'

    assert options.verbose
