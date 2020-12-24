

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
    print('S -> NP VP'  in grammar_set)
    print('NP -> Det N' in grammar_set)
    print('VP -> V NP' in grammar_set)
    print('V -> ate' in grammar_set)
    print('NP -> john' in grammar_set)
    print('Det -> a' in grammar_set)
    print('N -> sandwich' in grammar_set)



if __name__ == '__main__':
    main()
