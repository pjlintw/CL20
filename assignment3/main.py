

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

def main():
    import nltk
    from nltk.tree import Tree


    grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg") 
    grammar = nltk.data.load("atis//atis.cfg") 
    #cng_grammar = grammar.chomsky_normal_form()

    print(type(cng_grammar))



if __name__ == '__main__':
    main()
