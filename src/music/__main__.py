import sys

from .app import run_app
from .library import Library
from .find_cue_sheet_paths import find_cue_sheet_paths
from .options import Options
from .write_report import write_report


options = Options.parse()
library = Library.load(options.root)
paths = find_cue_sheet_paths(options.root)

if options.app:
    run_app(library)
else:
    write_report(options.root, paths, sys.stdout, options.verbose)
