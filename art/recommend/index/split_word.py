import MeCab

wakati = MeCab.Tagger("-Owakati")


def split_text(text: str):
    return wakati.parse(text).split()
