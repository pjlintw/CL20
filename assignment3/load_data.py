import nltk
nltk.download('large_grammars', download_dir='./')

grammar = nltk.data.load("grammars/large_grammars/atis.cfg")
s = nltk.data.load("grammars/large_grammars/atis_sentences.txt")
t = nltk.parse.util.extract_test_sentences(s)
