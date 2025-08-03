from pathlib import Path

from music.app import App
from music.library import Library


root = Path("~/Dropbox/Music/Don's Music").expanduser()
library = Library.load(root)
app = App(library)
app.run()
