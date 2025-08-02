from music.library import Track

from .model_list import ModelList


class TracksList(ModelList[Track]):
    def __init__(self):
        super().__init__('track')

    def model_text(self, model: Track) -> str:
        return str(model.title)

    def sort_models(self, models: list[Track]) -> list[Track]:
        return sorted(models, key=lambda model: model.title)
