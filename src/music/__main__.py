import sys

from .app import App
from .library import Library
from .find_cue_sheet_paths import find_cue_sheet_paths
from .options import Options
from .write_report import write_report


options = Options.parse()
library = Library.load(options.root)

if options.app:
    app = App(library)
    app.run()
else:
    paths = find_cue_sheet_paths(options.root)
    write_report(options.root, paths, sys.stdout, options.verbose)
