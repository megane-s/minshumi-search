import pickle
import random
import time

index = {}
for i in range(1_000_000):
    id = f"id-{i}"
    numbers_len = random.randrange(20)
    numbers = [f"word-{random.randrange(10)}" for _ in range(numbers_len)]
    for number in numbers:
        if str(number) in index:
            index[str(number)].append(id)
        else:
            index[str(number)] = [id]

with open("./index", "wb") as f:
    pickle.dump(index, f)

with open('./index', 'rb') as f:
    index = pickle.load(f)

while True:
    q = input("q=")
    if q == "q":
        break
    start = time.time()
    res = index[q][0:10] if q in index else None
    end = time.time()
    print(res, f"{end-start}s")
