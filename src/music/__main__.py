import sys

from .app import run_app
from .find_cue_sheet_paths import find_cue_sheet_paths
from .options import Options
from .write_report import write_report


options = Options.parse()
paths = find_cue_sheet_paths(options.root)

if options.app:
    run_app(options.root, paths)
else:
    write_report(options.root, paths, sys.stdout, options.verbose)
