"""
This CKY algorithm for recognizing language and syntatic parsing.
The parsing function designs for the grammar which has Chomsky normal (CNF) form and *don't* handle unary rule,
i.e. all production rules are of the form A -> B C, or A -> "token".
Make sure the production rules file is in CNF.

Feature: we construct a Node object as a Tree to record the root node and subnodes.
It allows us to backtrace all previous nonterminal node until terminal symbol.


"""

import pprint
from collections import defaultdict
import time

pp = pprint.PrettyPrinter(depth=4)

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

    we collect the nonterminal symbols for tokens and substring.
    chart[i][j] represents its nontermial and can access its 
    token or the two subnodes by the nonterminal key.
            chart[i][j][A]: [(BC, k_1), (BC, k_2)]
    backpointers: 

    """
    def add_rule_to_dict(rule_dict, lhs, rhs):
        """Add production rule to (non-)terminal rule dictionary.

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
        lhs, rhs = lhs.strip(), rhs.strip()
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
    return grammar, nonterminal_symbol


def parse_fn(sentences):
    """Preprocessing sentences of list. 

    Args:
      sentences:
    """
    def _parse(sentence):
        lower_sent = sentence.lower()
        s = '\"{}\"'
        double_quto_tokens = [ s.format(tok) for tok in lower_sent.strip().split()]
        return double_quto_tokens 
    for sent in sentences:
        yield _parse(sent)


def run_cky_wrapper(parser, sent_lst, output='output.o'):
    """CKY 

    Args:
      parser
      sent_lst: a list of sentence
      output: 
    Returns:
    """
    start = time.time()
    writer = open(output, 'w', encoding='utf-8')
    for sent in parse_fn(sent_lst):
        sent_len = len(sent)

        # chart[0][sent_len]
        roots = parser.parse(sent)
        trees = [prod for prod in roots if prod._root == 'SIGMA']
        num_trees = len(trees)

        sent_str = ' '.join(sent).replace('\"', '') 
        writer.write(f'{sent_str}\t{num_trees}\n')
        
        # t = backtracer(tree)
        # t_nltk = Tree.fromstring(t)
        # t_nltk.draw()
    print(f'Create file to path: {output}')
    print(f'executed {time.time()-start}')
        
    # sent_str = ' '.join([ tok.replace('\"', '') for tok in sent])
    # if isInLanuage:
    #     print(f'sentence, \"{sent_str}\", in language')
    # else:
    #     print(f'sentence, \"{sent_str}\", not in language')
    #     print(sys_info)

class Node:
    """a Node class represents tree."""
    def __init__(self, root, left, right, end):
        """Consturct a node of substree with root, left, right,
        and terminal symbol variable.

        Args:
          root: string, a root node of tree
          left: string, left hand side child
          right: string, right hand side child
          end: string, terminal symbol (token)
        """
        self._root = root
        self._left = left
        self._right = right
        self._terminal = end
        

class CKYParser:
    def __init__(self, grammar):
        super(CKYParser, self).__init__()
        self.grammar = grammar
        self.chart = None

    @staticmethod
    def check_coverage(self, sents, grammar):
        """Check grammar covers token.

        Args:
          sent: tokens of list
        Returns:
        """
        notCover = [1 for t in tokens if t not in grammar]
        if notCover:
            raise ValueError("Grammar does not cover some of the input words:")
    

    def recognize(self, sent, chart):
        """Check if the given input is in language
    
        1. unknown words
        2. can not derive to `S` 
        """
        if not self.chart:
            print('chart is none')

        return None

    def parse(self, sent):
        """CKY parse for a sentence with chart.

        Args:
          sent: list of tokens 
          grammar:

        Returns:
          chart: 3D lists,
        """
        sent_len = len(sent)
        # Chart with shape (n+1, n+1)
        # Each cell in chart[i][k] keeps one or more than one non-terminal symbol representing a substring
        # sentence[i][k] represents a list of substring from i to k-1.
        chart = [ [ set() for _ in range(sent_len+1)] for _ in range(sent_len+1)]
        # back_chart = [ [ defaultdict(lambda: list()) for _ in range(sent_len+1)] for _ in range(sent_len+1)]
        
        # span 1: (0,1), (1,2), ..., (n-1,n) 
        # span 2: (0,2), (1,3), ..., (n-2,n)
        # span n, (0,n)

        ### labels terminal symbols (token) with chart ###
        cl = list()
        for i in range(sent_len):
            tok = sent[i]
            if tok in self.grammar:
                # list of nonterminal
                nonterms = self.grammar[tok]
                # key(str): [token(str)]
                for nonterm in nonterms:
                    chart[i][i+1].add(Node(nonterm, None, None, tok))
                    
        
        ### labels substring with length from 2 to sentence length ###
        # span 2: [john|ate](0:1+1), [ate|a](1:2+1), [a|sandwitch](3:3+1)
        for span in range(2, sent_len+1):
            for begin in range(0, sent_len-span+1):
                end = begin + span
                for split in range(begin+1, end):
                    # print(f'span:{span}, begin:{begin}, split:{split}, end:{end}')
                    # add Node to chart[i][k] if A->BC in grammar
                    left_nonterms = chart[begin][split] 
                    right_nonterms = chart[split][end] 
                    for B in left_nonterms:
                        for C in right_nonterms:
                            # acess the nonterminal in string
                            b_string = B._root
                            c_string = C._root
                            children = '|'.join([b_string, c_string])
                            children = '|'.join([b_string, c_string])
                            if children in self.grammar:
                                parents = self.grammar[children]
                                for parent in parents:
                                    chart[begin][end].add(Node(parent, B, C, None))
        self.chart = chart
        return self.chart[0][sent_len]


    def backtracer(self, root_node):
        """Recursively backtracing a parsing tree starting from an Node object.

        Args:
          root_node: Node object. 
        Returns:
          string, parsing tree can be construct a nltk.Tree object
        """
        if root_node._terminal != None:
            return f'({root_node._root} {root_node._terminal})'
        else:
            lhs_node, rhs_node = root_node._left, root_node._right
            lhs = self.backtracer(lhs_node)
            rhs = self.backtracer(rhs_node)
            return f'({root_node._root} {lhs} {rhs})'


def main():
    grammar_file = 'atis/atis-grammar-cnf.cfg'
    toy_grammar_file = 'toy_data/toy-grammar.txt'
    toy_grammar_file2 = 'toy_data/atis-grammar-cnf.cfg'

    toy_sent_file = 'toy_data/toy-sentences.txt'
    toy_one_sent_file = 'toy_data/toy-one-sentence.txt'
    toy_five_sent_file = 'toy_data/toy-5-sentence.txt'

    sent_file = 'atis/atis-test-sentences.txt'

    #grammar = nltk.data.load("grammars/atis-grammar-cnf.cfg") 
    # grammar = nltk.data.load("atis/atis-grammar-cnf.cfg") 
    #cng_grammar = grammar.chomsky_normal_form()

    #print(grammar)

    ###
    # toy example
    ###
    grammar, _ = create_product_rule(grammar_file)

    #
    parser = CKYParser(grammar)
    #

    num_grammar = 0
    for k in grammar:
        num_grammar += len(grammar[k])
    print('num grammar', num_grammar)
    print()
    test_sent = load_data(toy_five_sent_file)
    
    # write sentence and its number of trees to file 
    # the parser will recognize sentence if not in grammar or in lanugage
    run_cky_wrapper(parser, test_sent)

    
if __name__ == '__main__':
    main()
