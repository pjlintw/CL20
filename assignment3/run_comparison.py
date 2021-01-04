import os
import pprint
import argparse
from nltk.tree import Tree
from nltk.draw.tree import TreeView
from parser import *
import pandas as pd
import matplotlib.pyplot as plot

pp = pprint.PrettyPrinter(depth=4)


def test_backtrace_time(parser, sent_lst, output='comparison.o'):
    """Get running time do and without backtracing."""
    # Collect running time of 
    without_backtrace = list()
    with_backtrace = list()
    
    output_folder = 'result'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, output)
    writer = open(output_path, 'w', encoding='utf-8')

    processed_sent_lst = parse_fn(sent_lst)
    for idx, sent in enumerate(processed_sent_lst):
        sent_len = len(sent)
        
        # time 
        start = time.time()
        roots = parser.parse(sent)
        trees = [prod for prod in roots if prod._root == 'SIGMA']
        num_trees = len(trees)
        before_backtrace = time.time()
        # skip if no tree
        if num_trees == 0:
            continue
        # Get list of trees from root node
        tress_lst = parser.build_trees_from_node(roots)
        after_backtrace = time.time()
    
        with_backtrace.append((num_trees, after_backtrace-start))
        without_backtrace.append((num_trees, before_backtrace-start))

        sent_str = ' '.join(sent).replace('\"', '') 
        writer.write(f'{sent_str}\t{num_trees}\t{before_backtrace-start}\t{after_backtrace-start}')
    writer.close()

    return with_backtrace,without_backtrace

def main():
    # Test file 
    file_path = 'data/atis-test-sentences-100.txt'

    # Grammar file
    grammar_file = 'data/atis-grammar-cnf.cfg'

    # Load grammar from file
    grammar = create_product_rule(grammar_file)

    # Construct CKYParser from grammar
    parser = CKYParser(grammar)

    # Visualize
    test_sent = load_data(file_path)
    with_backtrace, without_backtrace = test_backtrace_time(parser=parser, sent_lst=test_sent)
    
    idx_lst = [ ele[0] for ele in without_backtrace]
    with_backtrace = [ ele[1] for ele in with_backtrace]
    without_backtrace = [ ele[1] for ele in without_backtrace]
    
    df = pd.DataFrame({
        'Without backtracing': without_backtrace,
         'Do backtracing': with_backtrace
            }, index=idx_lst)
    
    lines = df.plot.line(style=['bs-','ro-'])
    plot.show()


if __name__ == '__main__':
    main()
