import pickle

with open('words.pickle', 'rb') as f:
    words_dict = pickle.load(f)
words_set = set(words_dict.values())
with open('words_set.pickle', 'wb') as f:
    words_set = pickle.dump(words_set, f)
