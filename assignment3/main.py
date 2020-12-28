"""
This CKY algorithm for recognizing language and syntatic parsing.
The parsing function designs for the grammar which has Chomsky normal (CNF) form and *don't* handle unary rule,
i.e. all production rules are of the form A -> B C, or A -> "token".
Make sure the production rules file is in CNF.
"""

import pprint
from collections import defaultdict
import numpy as np

pp = pprint.PrettyPrinter(depth=4)

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
        rhs = rhs.strip()
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
    #print(grammar)
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


def backtracer(chart):
    """Backtracing the parsing trees from given chart.

    Args:
      chart: ...
    Returns:
    """
    return None


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
    # Chart(i, k) with shape (n+1, n+1)
    # Each cell in chart[i][k] keeps one or more than one non-terminal symbol representing a substring
    # sentence[i][k] represents a list of substring from i to k-1.
    chart = [ [ defaultdict(lambda: list()) for _ in range(sent_len+1)] for _ in range(sent_len+1)]
    # span 1: (0,1), (1,2), ..., (n-1,n) 
    # span 2: (0,2), (1,3), ..., (n-2,n)
    # span n, (0,n)

    ### labels terminal symbols (token) with chart ###
    for i in range(sent_len):
        tok = sent[i]
        if tok in grammar:
            # list of nonterminal
            nonterms = grammar[tok]
            # key(str): [token(str)]
            for nonterm in nonterms:
                chart[i][i+1][nonterm].append(tok)
            
            print('span 1', sent[i:i+1])
            pprint.pprint(dict(chart[i][i+1]))
            print()
        else:
            sys_info = f'token {tok} not in grammar'
            return isInLanguage, sys_info

    
    ### labels substring with length from 2 to sentence length ###
    # span 2: [john|ate](0:1+1), [ate|a](1:2+1), [a|sandwitch](3:3+1)
    # span 2: [john|ate a], [john ate| a]
    for span in range(2, sent_len+1):
        for begin in range(0, sent_len-span+1):
            end = begin + span
            for split in range(begin+1, end):
                print(f'span:{span}, begin:{begin}, split:{split}, end:{end}')
                print(f'substrings:{sent[begin:split]}, {sent[split:end]}')
                
                left_nonterms = chart[begin][split]
                right_nonterms = chart[split][end]

                ### check ###
                # chart[i][j][A] = ['token'] == sent[i:j]
                if span == 2:
                    tok = sent[begin:end]
                    #print('span 2, substring', tok)
                    #print_defaultdict(left_nonterms)
                    #print()
                    for k in left_nonterms:
                        cur_tok = sent[begin:split]
                        #print('current token',cur_tok)
                        #print(cur_tok == left_nonterms[k])
                        assert cur_tok == left_nonterms[k]
                ### check ###
                   
                ### EXTRAX: ###
                # group subnodes and split k as tuple of (B|C, k)
                # add tuple to corresponding parent, if (B, C) as children of substree
                for B in left_nonterms:
                    for C in right_nonterms:
                        children = '|'.join([B, C])
                        # print('each BC', B,C)
                        # print('B C in grammar', children in grammar) 
                        if children in grammar:
                            parents = grammar[children]
                            for parent in parents:
                                tup = (children, split)
                                chart[begin][end][parent].append(tup)
                                #print('index of begin and end', begin, end)
                            # print(sent[begin:end])
                            # print(dict(chart[begin][end]))
                            # print()

                left_subs = sent[begin:split]
                right_subs = sent[split:end]
                # print(left_subs, right_subs)
                # print('chart[i][j]', end='\t')
                # print_defaultdict(chart[begin][end])
                
                ### print A-> BC, A-DE ###
                # for k in chart[begin][end]:
                #     num_sub = len(chart[begin][end][k])
                #     if num_sub > 1:
                #         print('num_sub greater than 1')
                #         print(begin, end)
                #         print('key', k)
                #         print(chart[begin][end][k])
                # print()
                
            pp.pprint(dict(chart[begin][end]))
            print()
        #print()
    # pp.pprint(chart[0][4])

    #trees, num_tree = backtracer(chart)

    print('end', end)
    roots = chart[0][end]
    if 'SIGMA' in roots:
        print('SIGMA' in roots) 
        print(roots['SIGMA'])
        print(len(roots['SIGMA']))
        print(len(roots['S']))
        isInLanguage = True
        return isInLanguage, sys_info

    return isInLanguage, sys_info

def printTable(myDict, colList=None):
   """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
   If column names (colList) aren't specified, they will show in random order.
   Author: Thierry Husson - Use it as you want but don't blame me.
   """
   if not colList: colList = list(myDict[0].keys() if myDict else [])
   myList = [colList] # 1st row = header
   for item in myDict: myList.append([str(item[col] if item[col] is not None else '') for col in colList])
   colSize = [max(map(len,col)) for col in zip(*myList)]
   formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
   myList.insert(1, ['-' * i for i in colSize]) # Seperating line
   for item in myList: print(formatStr.format(*item))

def main():
    import nltk
    from nltk.tree import Tree

    grammar_file = 'atis/atis-grammar-cnf.cfg'
    toy_grammar_file = 'toy_data/toy-grammar.txt'
    toy_grammar_file2 = 'toy_data/atis-grammar-cnf.cfg'

    toy_sent_file = 'toy_data/toy-sentences.txt'
    toy_one_sent_file = 'toy_data/toy-one_sentence.txt'

    #grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg") 
    # grammar = nltk.data.load("atis/atis-grammar-cnf.cfg") 
    #cng_grammar = grammar.chomsky_normal_form()

    #print(grammar)

    ###
    # toy example
    ###
    grammar, _ = create_product_rule(grammar_file)
    print('show', grammar['\"show\"'])
    print('the', grammar['\"the\"'])
    print('flights', grammar['\"flights\"'])
    print('.', grammar['\".\"'])

    num_grammar = 0
    for k in grammar:
        num_grammar += len(grammar[k])
    print('num grammar', num_grammar)
    print()


    ### recognize sentence ###
    test_sent = load_data(toy_one_sent_file)
    for sent in parse_fn(test_sent):
        isInLanuage, sys_info = recognize(sent, grammar)
        sent_str = ' '.join([ tok.replace('\"', '') for tok in sent])
        if isInLanuage:
            print(f'sentence, \"{sent_str}\", in language')
        else:
            print(f'sentence, \"{sent_str}\", not in language')
            print(sys_info)

    s = ['show', 'the', 'flights', '.']


    ## 2, 3, 2, 2, 2, 200
if __name__ == '__main__':
    main()
