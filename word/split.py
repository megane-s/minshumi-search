import MeCab

parser = MeCab.Tagger("-Owakati")


def word_split(text: str) -> list[str]:
    return parser.parser(text).split()
