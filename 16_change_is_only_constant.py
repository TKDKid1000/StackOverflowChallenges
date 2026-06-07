import json
import math
from typing import Generator

with open("Challenge16.txt") as f:
    inputs = json.load(f)


# Recursively loops `counts`, basically nesting the loop to its length
def combinations(counts: list[int]) -> Generator[tuple[int, ...]]:
    def recurse(idx: int, combos: list[int]) -> Generator[tuple[int, ...]]:
        if idx == len(counts):
            yield tuple(combos)
            return
        for i in range(counts[idx] + 1):
            combos.append(i)
            yield from recurse(idx + 1, combos)
            combos.pop()

    yield from recurse(0, [])


def minimize_coins(
    denominations: list[int], counts: list[int], target: int
) -> tuple[int, ...] | None:
    # Immediately impossible due to too few coins
    if sum(denominations[i] * counts[i] for i in range(len(counts))) < target:
        return None

    com_denom = math.gcd(*denominations)
    # Immediately impossible due to too improper factorization
    if target % com_denom != 0:
        return None

    min_size = -1
    min_combo = None
    for combo in combinations(counts):
        value = sum(denominations[i] * combo[i] for i in range(len(counts)))
        if value == target and (min_size == -1 or sum(combo) < min_size):
            min_size = sum(combo)
            min_combo = combo

    return min_combo


result = []
# print(minimize_coins(np.array([1, 7, 10]), np.array([10, 2, 1]), 14))
for i in inputs:
    print("###:", i)
    minimized = minimize_coins(i[0], i[1], i[2])
    if minimized is None:
        print(-1)
        result.append(-1)
    else:
        print(sum(minimized), minimized)
        result.append(sum(minimized))

print(result)

