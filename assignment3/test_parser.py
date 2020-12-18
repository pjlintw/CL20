import nltk

grammar = nltk.data.load('grammars/large_grammars/atis.cfg')
atis_sent = 'grammars/large_grammars/atis_sentences.txt'
s = nltk.data.load(atis_sent)
t = nltk.parse.util.extract_test_sentences(s)

parser = nltk.parse.BottomUpChartParser(grammar)
for sentence in t:
    print(parser.chart_parse(sentence[0]))
