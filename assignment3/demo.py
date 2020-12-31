from parser import *

def main():
    grammar_file = 'atis/atis-grammar-cnf.cfg'

    # Load grammar from file
    grammar, _ = create_product_rule(grammar_file)

    # Construct CKYParser from grammar
    parser = CKYParser(grammar)

    # Check grammar covers tokens
    sentence = ['\"prices\"', '\".\"']
    isInGrammar = CKYParser.check_coverage(sentence, grammar)

    # All nonterminal results
    roots = parser.parse(sentence)

    # Check sentence 
    isInLanguage = parser.recognize(sentence)

    # Creat a tree in string format
    tree_list = parser.build_trees_from_node(roots)

    print('In the grammar :', isInGrammar)
    print('In the language:', isInLanguage)
    print('Trees:', tree_list)

if __name__ == '__main__':
    main()