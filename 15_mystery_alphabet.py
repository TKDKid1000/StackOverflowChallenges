with open("15_alphabet.txt") as f:
    myst_dict = [w.strip() for w in f.readlines()]

myst_alphabet = set("".join(myst_dict))
myst_ordered = []

for word in myst_dict:
    if len(myst_ordered) == 0 or myst_ordered[-1] != word[0]:
        myst_ordered.append(word[0])

print("Initial alphabet:")
print("".join(myst_ordered))
print(len(myst_ordered))

# Any letters not at the starts of words (⨙)
missing = set(myst_alphabet).difference(myst_ordered)

for m in missing:
    word_prefixes = []
    for word in myst_dict:
        if m not in word: continue
        word_prefixes.append(word[:word.index(m)])

    after = []
    before = []
    for prefix in word_prefixes:
        self_reached = False
        for word in myst_dict:
            if not word.startswith(prefix): continue

            char = word[len(prefix):len(prefix)+1]
            if char == m:
                self_reached = True
            elif self_reached:
                if char not in before:
                    before.append(char)
            else:
                if char not in after:
                    after.append(char)

    # Sort the before/after by the known alphabet
    after.sort(key=myst_ordered.index)
    before.sort(key=myst_ordered.index)

    # Find the best index using the last of before and first of after
    af, bf = after[-1], before[0]
    af_idx, bf_idx =myst_ordered.index(af), myst_ordered.index(bf)

    idx = (af_idx + bf_idx)//2 + 1

    myst_ordered.insert(idx, m)

print("Final alphabet:")
print("".join(myst_ordered))
print(len(myst_ordered))
