
from art.recommend.recommend import (get_recommend_index, get_vec_model,
                                     init_for_recommend)


def main():
    init_for_recommend()

    q = input("q:")
    model = get_vec_model()
    if q not in model.wv:
        print("検索結果なし (vectorize model にありませんでした)")
        return
    q_vec = model.wv[q]
    print("wv", q_vec)

    index = get_recommend_index()
    n, d = index.query(q_vec, k=20)
    print(n)
    print(d)


main()
