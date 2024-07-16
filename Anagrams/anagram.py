import itertools


with open('wordlist.txt') as f:
    word_set = set(f.read().splitlines())


def anagrams(word):
    word_sorted = sorted(word)
    ana_lst = set(w for w in word_set if sorted(w)==word_sorted)
    return ana_lst

def find_anagrams(word):
    anagrams = []
    for i in range(3, len(word)+1):
        for subset in itertools.permutations(word, i):
            subset_word = ''.join(subset)
            if subset_word in word_set:
                anagrams.append(subset_word)
    anagrams.reverse()
    return anagrams