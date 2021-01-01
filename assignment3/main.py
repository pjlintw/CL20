"""
This CKY algorithm for recognizing language and syntatic parsing.
The parsing function designs for the grammar which has Chomsky normal (CNF) form and *don't* handle unary rule,
i.e. all production rules are of the form A -> B C, or A -> "token".
Make sure the production rules file is in CNF.

Feature: we construct a Node object as a Tree to record the root node and subnodes.
It allows us to backtrace all previous nonterminal node until terminal symbol.
"""
import os
import argparse
import pprint

from parser import *

pp = pprint.PrettyPrinter(depth=4)


def run_cky_wrapper(parser, sent_lst, output='output.o'):
    """Evauluating CKY parser on list of sentence and save 
    the sentence and number of trees to output file.

    Args:
      parser: CKYParser object
      sent_lst: a list of sentence
      output: file with the form sentence and number
    """
    output_folder = 'result'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, output)
    # time 
    start = time.time()
    writer = open(output_path, 'w', encoding='utf-8')

    processed_sent_lst = parse_fn(sent_lst)
    for idx, sent in enumerate(processed_sent_lst):
        sent_len = len(sent)
        roots = parser.parse(sent)
        trees = [prod for prod in roots if prod._root == 'SIGMA']
        num_trees = len(trees)

        sent_str = ' '.join(sent).replace('\"', '') 
        writer.write(f'{sent_str}\t{num_trees}\n')
    num_sent = idx + 1
    writer.close()
    print(f'Create file to path: {output_path}')
    print(f'Parsing {num_sent} sentences for {time.time()-start} secs.')
    print(f'Saving file to {output_path}')


def run_tree_drawer(parser, sent_lst, show=False, output_folder='img'):
    """Draw one parsing tree for each sentence. 

    Args:
      parser:
      sent_lst: list of sentences
      show: boolean, if draw the tree
      output_folder: path for saving .ps files
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    processed_sent_lst = parse_fn(sent_lst) 
    for idx, sent in enumerate(processed_sent_lst):
        roots = parser.parse(sent)
        trees = [prod for prod in roots if prod._root == 'SIGMA']
        tree_str = parser.backtracer(trees[0])
        t = Tree.fromstring(tree_str)

        if show:
            t.draw()

        path = os.path.join(output_folder, f'tree-{idx}.ps')
        TreeView(t)._cframe.print_to_file(path)
        print(f'Saving tree image to {path}')


def main():
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("--count_tree")
    parser.add_argument("--draw_tree")
    args = parser.parse_args()

    # Grammar file
    grammar_file = 'data/atis-grammar-cnf.cfg'

    # Load grammar from file
    grammar, _ = create_product_rule(grammar_file)

    # Construct CKYParser from grammar
    parser = CKYParser(grammar)

    # Write sentence and its number of trees to file 
    # The parser will recognize sentence if 
    # not in grammar or in lanugage.
    if args.count_tree:
        file_path = args.count_tree
        test_sent = load_data(file_path)
        run_cky_wrapper(parser=parser, sent_lst=test_sent)

    # Draw parsing tree and save image to path `/img/.`
    if args.draw_tree:
        file_path = args.draw_tree
        test_sent = load_data(file_path)
        run_tree_drawer(parser=parser, sent_lst=test_sent, show=False)


if __name__ == '__main__':
    main()
