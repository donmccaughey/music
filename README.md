# Music

-- ♫ --


## Development Setup

1. Install `make`
2. Install `pyenv` and `pyenv-virtualenv`
3. Create a `music-venv` virtual environment using Python 3.12.1 and activate it
4. `pyenv install 3.12.1` to install a recent Python version.
5. `pyenv virtualenv 3.12.1 music-venv` to create a virtualenv for this project.
6. Edit the `.python-version` file, setting the version to `music-venv`.
7. In PyCharm's *Preferences* dialog, select 
     *Project: Music | Python Interpreter* in the tree of options and choose  
     `music-venv` as the Python version.
8. Run tests: `make check`

Update a virtual environment:

1. `cd <project-dir>`
2. `pyenv virtualenv-delete <venv-name>`
3. `pyenv install --list` to list available Python versions.
4. `pyenv install <python-version>` to install a recent Python version.
5. `pyenv virtualenv <python-version> <venv-name>`
6. `pip install --upgrade pip`
7. `pip install -r requirements.txt`
7. `pip install -r requirements-dev.txt`
