
from art.get import get_all_arts


class ArtTitleIterable:
    def __iter__(self):
        for art in ArtIterable():
            yield art.title


class ArtIterable:
    # TODO
    def __iter__(self):
        for art in get_all_arts():
            yield art
