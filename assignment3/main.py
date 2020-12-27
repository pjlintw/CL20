"""
This CKY algorithm for recognizing language and syntatic parsing.
The parsing function designs for the grammar which has Chomsky normal (CNF) form and *don't* handle unary rule.
Make sure the production rules file is in CNF.
"""

from pprint import pprint 
from collections import defaultdict


def load_data(path):
    with open(path) as f:
        return f.readlines()


def print_defaultdict(defaultDict):
    """Print defaultdict with its type."""
    print(dict.__repr__(defaultDict))


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

    we collect the nonterminal symbols for tokens and substring.
    chart[i][j] represents its nontermial and can access its 
    token or the two subnodes by the nonterminal key.
            chart[i][j][A]: [(BC, k_1), (BC, k_2)]
    backpointers: 

    """
    def add_rule_to_dict(rule_dict, lhs, rhs):
        """Add production rule to (non-)terminal-rule dictionary.

        Args:
          rule_dict: dict, mapping terminal symbol or two nonterminal o one nonterminal
          lhs: rule of right hand site
          rhs: rule of left hand site
        Returns:
          rele_dict: the left-hand-sided to right-hand-sided term mapping.

          :production rules:
          SIGMA  -> QUANP_DTI CJC
          NP_NNS -> QUANP_DTI CJC

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
      sys_info: string for reason why not in language
    """
    isInLanguage = False
    sys_info = ''

    sent_len = len(sent)
    # Chart(i, k)
    # Each cell in chart[i][k] keeps one or more than one non-terminal symbol representing a substring
    chart = [ [ defaultdict(lambda: list()) for _ in range(sent_len+1)] for _ in range(sent_len+1)]    

    ### labels terminal symbols (token) with chart ###
    for i in range(sent_len):
        tok = sent[i]
        if tok in grammar:
            # list of nonterminal
            nonterms = grammar[tok]
            #print(nonterms)
            #
            # print(type(nonterms))
            # print(nonterms)
            # key(str): [token(str)]
            for nonterm in nonterms:
                chart[i][i+1][nonterm].append(tok)
        else:
            sys_info = 'token not in grammar'
            return isInLanguage, sys_info
            
    ### labels substring with length from 2 to sentence length ###
    # span 2: [john|ate](0:1+1), [ate|a](1:2+1), [a|sandwitch](3:3+1)
    # span 2: [john|ate a], [john ate| a]
    for span in range(2, sent_len+1):
        for begin in range(0, sent_len-span+1):
            end = begin + span
            for split in range(begin+1, end):
                print(f'span:{span}, begin:{begin}, split:{split}')
                # left_substring[begin][split]
                # right_substring[right][end]
                print(f'left substring:{sent[begin:split]},{sent[split:end]}')
                print('left', type(chart[begin][split]))
                print('right', type(chart[split][end-1]))
                #left_substring = sent[begin:split]
                #right_substring = sent[split:end]
                
                left_nonterms = chart[begin][split]
                right_nonterms = chart[split][end]

                ### check ###
                # chart[i][j][A] = ['token'] == sent[i:j]
                if span == 2:
                    for k in left_nonterms:
                        cur_tok = sent[begin:split]
                        print('current token',cur_tok)
                        print(cur_tok == left_nonterms[k])
                        assert cur_tok == left_nonterms[k]
                ### check ###
                   
                print_defaultdict(left_nonterms)
                print_defaultdict(right_nonterms)
                
                ### EXTRAX: ###
                # group subnodes and split k as tuple of (B|C, k)
                # add tuple to corresponding parent, if (B, C) as children of substree
                for B in left_nonterms:
                    for C in right_nonterms:
                        children = '|'.join([B, C])
                        print('each BC', B,C)
                        print('B C in grammar', children in grammar) 
                        if children in grammar:
                            parents = grammar[children]
                            for parent in parents:
                                tup = (children, split)
                                chart[begin][end][parent] = tup
                                print('index of begin and end', begin, end)
                            print(sent[begin:end])
                            print(dict(chart[begin][end]))
                            print()
                #             pass
                print
            print()
        print()
    roots = chart[0][end]
    print_defaultdict(roots)

    if 'S' in roots:
        print('S' in roots) 
        isInLanguage = True
        return isInLanguage, sys_info

    return isInLanguage, sys_info


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
    # toy example
    ###
    grammar, _ = create_product_rule(toy_grammar_file)

    ### recognize sentence ###
    test_sent = load_data('toy_data/toy-sentences.txt')
    for sent in parse_fn(test_sent):
        isInLanuage, sys_info = recognize(sent, grammar)
        
        sent_str = ' '.join([ tok.replace('\"', '') for tok in sent])
        if isInLanuage:
            print(f'sentence, \"{sent_str}\", in language')
        else:
            print(f'sentence, \"{sent_str}\", not in language')
            print(sys_info)


if __name__ == '__main__':
    main()
