from music.library import Album

from .model_list import ModelList


class AlbumList(ModelList[Album]):
    def __init__(self):
        super().__init__('album')

    def model_text(self, model: Album) -> str:
        return str(model.title)

    def sort_models(self, models: list[Album]) -> list[Album]:
        return sorted(models, key=lambda model: model.title)
