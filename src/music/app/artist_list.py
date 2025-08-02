from music.library import Artist

from .model_list import ModelList


class ArtistList(ModelList[Artist]):
    def __init__(self):
        super().__init__('artist')

    def model_text(self, model: Artist) -> str:
        return str(model.name)

    def sort_models(self, models: list[Artist]) -> list[Artist]:
        return sorted(models, key=lambda model: model.name)
