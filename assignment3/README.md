# CL20: Assignment 3

This CKY parser desgins for recognizing language and syntatic parsing. The algorithm based on a chart for recording the nonterminal of a substring. We construct a Node object as a node (tree) to record the root node and subnodes. It allows us to backtrace all previous nonterminal node until terminal symbol.


## Setup and Data

1. python version and dependencies 

We uses python 3.7. Before execute file, please install the dependencies:
`pip install -r requirements.txt`

2. prepare data

The implementation utilise grammar file and sentence file under the `data` folder. Make sure those files are included.

### grammar

The CKY parser is designed for the grammar which has Chomsky normal (CNF), i.e. all production rules are of the form A -> B C, or A -> "token". Please make sure the grammar file `atis-grammar-original.cfg` is under the `data` folder.

The ATIS grammar in CNF is the file that each line of the grammar contains a production rule separating by arrow symbol `->`  and one nonterminal symbol on left hand side.

### sentence

`atis-test-sentences-100.txt`.  The sentences file consists of 100 sentences for testing parser. 98 sentences are from test set of for ATIS grammar and 2 additional are ungrammatical sentences.

`atis-test-sentences-draw.txt`.  The file consists of 5 sentencs which was randomly selected from ATIS test set for drawing parsing tree derived from the parser. 


## Run CKY Parer

### Basic Usage

The CKYParser performs sentence parsing, tree building in the script `demo.py`.

```
python demo.py
```

```python
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

# Output
print('In the grammar :', isInGrammar)
print('In the language:', isInLanguage)
print('Trees:', tree_list)
```

The output will look like this:
```
In the grammar : True
In the language: True
Trees: ['(SIGMA (NOUN_NNS "prices") (pt_char_per "."))', '(SIGMA (VERB_VBZ "prices") (pt_char_per "."))']
```

### Evaluating CKY parser on ATIS sentences 

The implementation of CKY parser supports to parse the ATIS sentences, compute the number of trees, and draw
one tree for each test sentence.

The example code will evaluate the CKY parser on the files provided by the flags `--count_tree`  and `--draw_tree`. A result file `result/output.txt` has the form of sentences and number of trees for each test sentence from the argument `--count_tree`. For plotting the parsing tree, the parser will plotting one of all possible trees for each test sentence from the file of `--draw_tree`. The plotting will be saved in the path `/img/`. 

```
python main.py \
  --count_tree=data/atis-test-sentences-100.txt \
  --draw_tree=data/atis-test-sentences-draw.txt
```

Note that the CKY parser will parse the `atis-test-sentences-100.txt` file for roughyl 9 minutes. We sugguest you to replace it with a smallar file `atis-test-sentences-draw.txt`. The grammar file `atis-grammar-cnf.cfg` is included in the code. The code will load the grammar.

```
python main.py \
  --count_tree=data/atis-test-sentences-draw.txt
```

### Runtime with and without backtracking

We visualize the runtime of executing backtracking and without executing. The x-axis is number of trees and y-axis runtime in the unit of second. The plotting shows no difference because the implementation of cky parser stores every substree in the chart. For example, left hand side nontermial A will be seen as different subtree in the chart if one of its children nodes or grandchildren is another nontermial symbol. Therefore, we can directly compute the number of `SIGMA` in the node for the whole sequence without doing backtracing. 

The plotting shows that the most time-consuming part is the production process. In the future, we will optimize the runtime by constructing the bottom up parsing 
with other implementation. 

!(plot)[img/Figure_1.png]

To plot the figure, run the `run_comparison.py` in the command line. Note that the program runs on the 100 sentences file. It will take 9 minutes for parsing all the possible trees of sentences.

```
python run_comparison.py
```

