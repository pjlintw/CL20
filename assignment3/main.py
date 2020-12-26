"""
This CKY algorithm for recognizing language and syntatic parsing.
The parsing function designs for the grammar which has Chomsky normal (CNF) form and *don't* handle unary rule.
Make sure the production rules file is in CNF.





"""


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

def create_product_rule(path):
    """Create grammar for terminal and non-terminal in CNF.

    Args:
      path: path to production rules in CNF.

    Examples:   

    terminal rule: {'"token1"':（[0.5, 0.5], ['NP', 'SIGMA']),
                    '"token2"': ([1.0]     , ['V']          )}
    nonterminal rule: {'Det N': ([1.0]     , ['NP']         ),
                       'V NP' : ([1.0]     , ['VP']         )'}

    toks:  ['tok1', 'tok2', 'tok3']
    chart: [ [{}, {}, {}]
             [{}, {}, {}]
             [{}, {}, {}]]

    backpointers: 

    """
    def add_rule_to_dict(rule_dict, lhs, rhs):
        """Add production rule to (non-)terminal-rule dictionary.

        Args:
          rule_dict: dict, mapping terminal symbol or two nonterminal o one nonterminal
          lhs: rule of right hand site
          rhs: rule of left hand site
        Returns:
          rele_dict: the right-hand-sided to the left-hand-sided term mapping.

          {'QUANP_DTI|CJC': ['SIGMA', 'NP_NNS'], '"gave"': ['pt_verb_vbd', 'VERB_VBD']}
        """
        if rhs not in rule_dict:
            rule_dict[rhs] = list()
            
        rule_dict[rhs].append(lhs)           
        return rule_dict

    # grammar {'"token1"': ['V', 'SIGMA'], 'V|NP': ['VP']}
    grammar = dict()
    nonterminal_symbol = set()
    for line in load_data(path):
        lhs, rhs = line.split('->')
        lhs = lhs.strip()
        rhs = [ tok for tok in rhs.split() if tok !='']

        # add nonterminal symbol
        nonterminal_symbol.add(lhs)
        if len(rhs) == 1:
            tok = rhs[0]
            assert '\"' in tok
            # add production rule
            add_rule_to_dict(grammar, lhs, tok)
        elif len(rhs) == 2:
            jointed_rhs = '|'.join(rhs)
            # add production rule
            add_rule_to_dict(grammar, lhs, jointed_rhs)
            #print(grammar)
        else:
            print('production rule not in CNF', line)
    print(grammar)
    return grammar, nonterminal_symbol

def parse_fn(sentences):
    """

    Args:
      sentences: () 
    """
    def _parse(sentence):
        lower_sent = sentence.lower()
        s = '\"{}\"'
        double_quto_tokens = [ s.format(tok) for tok in lower_sent.strip().split()]
        return double_quto_tokens 
    for sent in sentences:
        yield _parse(sent)

def recognize(sent, grammar):
    """CKY recognizer for a sentence

    Args:
      sent: list of tokens 
      grammar:

    Returns:
      isInLanguage: boolean, if the sentence in the language
    """
    isInLanguage = False

    sent_len = len(sent)
    # Chart(i, k)
    # Each cell in chart[i][k] keeps one or more than one non-terminal symbol representing a substring
    chart = [ [ {} for _ in range(sent_len)] for _ in range(sent_len)]    

    for i in range(sent_len):
        tok = sent[i]
        print(tok)
    
    # print('0,0', sent[0:0])
    # print('0,1', sent[0:1])

    # print('1,1', sent[1:1])
    # print('1,2', sent[1:2])

    ### labels terminal symbol A -> "token_i" ###
    # for tok_i in range(sent_len):
    #     for prod_rule in grammar:
    #         print(prod_rule)

    ### labels substring with length from 2 to sentence length ###
    for span in range(2, sent_len):
        for begin in range(0, sent_len-span):
            end = begin + span
            for split in range(begin, end+1):
                pass

    return isInLanguage


def main():
    import nltk
    from nltk.tree import Tree

    grammar_file = 'atis/atis-grammar-cnf.cfg'
    toy_grammar_file = 'toy_data/toy-grammar.txt'

    #grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg") 
    # grammar = nltk.data.load("atis/atis-grammar-cnf.cfg") 
    #cng_grammar = grammar.chomsky_normal_form()

    #print(grammar)

    ###
    # toy
    ###

    grammar, _ = create_product_rule(grammar_file)


    ### recognize sentence ###
    # test_sent = load_data('toy_data/toy-sentences.txt')
    # for sent in parse_fn(test_sent):
    #     isInLanuage = recognize(sent, grammar_set)
    #     print(isInLanuage)

    

if __name__ == '__main__':
    main()
