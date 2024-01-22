
from art.db.get import AllArts


class ArtTitleIterable:
    def __iter__(self):
        for art in ArtIterable():
            yield art.title


class ArtTagIterable:
    def __iter__(self):
        for art in ArtIterable():
            yield art.tags


class ArtIterable:
    # TODO
    def __iter__(self):
        for art in AllArts():
            yield art
