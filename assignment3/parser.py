"""Implement CKYParser class to parse the sentence and backtrace the tree. """

import os
import time


def load_data(path):
    """Load text file with one sentence per line."""
    with open(path) as f:
        return f.readlines()


def create_product_rule(path):
    """Create grammar for terminal and non-terminal in CNF.

    Args:
      path: path to the file of production rules in CNF.

    Returns:
      rule_dict: A dict mapping keys to the corresponding productions. For example:
          
      :production rules:
      SIGMA  -> QUANP_DTI CJC
      NP_NNS -> QUANP_DTI CJC

      {'QUANP_DTI|CJC': ['SIGMA', 'NP_NNS'], '"gave"': ['pt_verb_vbd', 'VERB_VBD']}
          
      Returned keys are production rule or token.Values are the its nonterminal symbols.  
    """
    def add_rule_to_dict(rule_dict, lhs, rhs):
        """Add production rule to dictionary.

        Add production rule and nonterminal to dict
        if don't have the key.

        Args:
          rule_dict: dict, mapping terminal symbol or production rule
                     to nonterminal
          lhs: rule of right hand side
          rhs: rule of left hand side

        Returns:
          rule_dict: a updated dict
        """
        if rhs not in rule_dict:
            rule_dict[rhs] = list()
        rule_dict[rhs].append(lhs)           
        return rule_dict

    grammar = dict()
    for line in load_data(path):
        lhs, rhs = line.split('->')
        lhs, rhs = lhs.strip(), rhs.strip()
        rhs = [ tok for tok in rhs.split() if tok !='']
        if len(rhs) == 1:
            tok = rhs[0]
            assert '\"' in tok
            # add production rule
            add_rule_to_dict(grammar, lhs, tok)
        elif len(rhs) == 2:
            jointed_rhs = '|'.join(rhs)
            # add production rule
            add_rule_to_dict(grammar, lhs, jointed_rhs)
        else:
            print('production rule not in CNF', line)
    return grammar # grammar {'"token1"': ['V', 'SIGMA'], 'V|NP': ['VP']}


def parse_fn(sentences):
    """Preprocessing list of sentences. 

    Remove the leading and trailing whitespaces 
    and add double quote to each token.

    Args:
      sentences: list of sentences
    """
    def _parse(sentence):
        lower_sent = sentence.lower()
        s = '\"{}\"'
        double_quto_tokens = [ s.format(tok) for tok in lower_sent.strip().split()]
        return double_quto_tokens 
    for sent in sentences:
        yield _parse(sent)


### EXTRA ###
class Node:
    """a Node class represents tree."""
    def __init__(self, root, left, right, end):
        """Consturct a node object to build a substree 
        with root, left, right and terminal symbol variables.

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
### EXTRA ###

class CKYParser:
    def __init__(self, grammar):
        super(CKYParser, self).__init__()
        self.grammar = grammar
        self.chart = None

    @staticmethod
    def check_coverage(sents, grammar):
        """Check grammar covers token.

        Args:
          sent: tokens of list
          grammar: A dict of production rule or token to nonterminal mapping
        Returns:
          isInGrammar: boolean, if the grammar covers the sentence
        """
        isInGrammar = True
        
        notCover = [1 for t in sents if t not in grammar]
        if notCover:
            print("Grammar does not cover some of the input words")
            isInGrammar = False
        return isInGrammar
    
    def recognize(self, sent):
        """Check if the given input is in language
    
        Args:
          sent: list of sentence
        Returns:
          isInLanguage: boolean, if the sentence can be derived to SIGMA
        """
        isInLanuage = True

        if not self.chart:
            roots = self.parse(sent)
        else:
            roots = self.chart[0][len(sent)]
        trees = [prod for prod in roots if prod._root == 'SIGMA']
        if not trees:
            isInLanuage = False
        return isInLanuage

        
    def build_trees_from_node(self, roots):
        """Build tree from a given node.

        Args:
          roots: the possible nonterminal of whole string in the chart.
        Returns:
          tree_lst: a collection of tree in string format.
        """
        trees = [prod for prod in roots if prod._root == 'SIGMA']

        tree_lst = list()
        for t in trees:
            tree_str = self.backtracer(t)
            tree_lst.append(tree_str)
        return tree_lst

    def parse(self, sent):
        """CKY parse for a sentence with chart.

        Args:
          sent: list of tokens added by double quote
          grammar: production rule and token to nonterminal mapping

        Returns:
          chart: A 3-D lists that collects all nonterminal symbol
          for all possible subtrings of a sentence. Chart[i][j]
          represents its nontermial and can hash its 
          token or the production rules by the nonterminal key.
          For example:            

          chart[i][j][A]: [(BC, k_1), (BC, k_2)]
        """
        sent_len = len(sent)
        # Chart with shape (n+1, n+1)
        # Each cell in chart[i][j] keeps one or more than one non-terminal symbol representing a substring
        # sentence[i][j] represents a list of substring from i to j-1.
        chart = [ [ set() for _ in range(sent_len+1)] for _ in range(sent_len+1)]
        
        ### labels terminal symbols (token) with chart ###
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
          root_node: Node object
        Returns:
          string, parsing tree in string format which 
          can be construct a nltk.Tree object
        """
        if root_node._terminal != None:
            return f'({root_node._root} {root_node._terminal})'
        else:
            lhs_node, rhs_node = root_node._left, root_node._right
            lhs = self.backtracer(lhs_node)
            rhs = self.backtracer(rhs_node)
            return f'({root_node._root} {lhs} {rhs})'





