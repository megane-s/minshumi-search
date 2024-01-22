from art.recommend import get_recommend_art, update_index

while True:
    cmd = input("update or search or q:")
    if cmd == "q":
        break
    if cmd == "update":
        update_index()
    if cmd == "search":
        print(get_recommend_art(input("query:")))
