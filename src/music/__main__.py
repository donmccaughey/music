import sys

from .find_cue_sheet_paths import find_cue_sheet_paths
from .options import parse_options
from .write_report import write_report


options = parse_options()
root = options.root.expanduser()
paths = find_cue_sheet_paths(root)
write_report(root, paths, sys.stdout, options.verbose)
