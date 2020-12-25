

class CKYRecognizer():
    def __init__(self, grammar):
        super.__init__()

    def recognize(self, tokens):
        """Check if the given input is in language
    
        1. unknown words
        2. can not derive to `S` 
        """
        return None

    def parse(self):
        return None

def load_data(path):
    with open(path) as f:
        return f.readlines()

def parse_fn(sentences):
    """

    Args:
      sentences: () 
    """
    def _parse(sentence):
        lower_sent = sentence.lower()
        return lower_sent.strip().split()
    for sent in sentences:
        yield _parse(sent)

def recognize(sent, grammar):
    """CKY recognizer for one sentence

    Args:
      sent: list of tokens 
      grammar:
    Returns:
      isInLanguage: boolean, if the sentence in the language
    """
    # Ch(i, k)
    ch = list()

    sent_len = len(sent)
    print(sent)

    ###
    for tok_i in range(sent_len):
        for prod_rule in grammar:
            pass

    #

def main():
    import nltk
    from nltk.tree import Tree


    #grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg") 
    # grammar = nltk.data.load("atis/atis-grammar-cnf.cfg") 
    #cng_grammar = grammar.chomsky_normal_form()

    #print(grammar)

    ###
    # toy
    ###
    grammar_lst = load_data('toy_data/toy-grammar.txt')
    grammar_set = set([item.strip() for item in grammar_lst])

    test_sent = load_data('toy_data/toy-sentences.txt')

    for sent in parse_fn(test_sent):
        isInLanuage = recognize(sent, grammar_set)
        print(isInLanuage)

    size =3
    chart = [[[] for _ in range(size) ] for _ in range(size)]
    import numpy as np
    print(np.array(chart).shape)

if __name__ == '__main__':
    main()
