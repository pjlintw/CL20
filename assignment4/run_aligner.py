"""Implementation of IBM model 1 aligner."""
import argparse
import sys
from collections import defaultdict

em_config = {'iteration': 1}

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', dest='train', default='hw2/data/hansards')
parser.add_argument('-e', '--english', dest='english', default='e') # target
parser.add_argument('-f', '--french', dest='french' , default='f') # source
parser.add_argument('-n', '--number', dest='num_sents', default=100)
args = parser.parse_args()

f_count = defaultdict(int)
e_count = defaultdict(int)
fe_count= defaultdict(int)

class Bitexter:
    """Create for bitext."""
    def __init__(self, f_data, e_data, num_sents=100):
        self.NULL_TOKEN = 'NULL'
        self.f_data = f_data
        self.e_data = e_data
        self.num_sents = num_sents
    
    def yield_pairs(self):
        """Generate sentence pair."""
        with open(self.e_data) as e_file, open(self.f_data, 'r') as f_file:
            num_example = 0
            for e_sent, f_sent in zip(e_file, f_file):
                num_example +=1
                # Stop if reachs number of sentence
                if num_example == self.num_sents+1:
                    break
                yield [self.NULL_TOKEN] + self.parse_sentence(e_sent), self.parse_sentence(f_sent)
    
    def parse_sentence(self, sentence):
        return sentence.strip().split()

    def build_vocab(self):
        """Build vocaburaries."""
        f_vocab = set()
        e_vocab = set()
        num_example = 0
        with open(self.f_data, 'r') as f_file, open(self.e_data) as e_file:
            for f_line, e_line in zip(f_file, e_file):
                num_example +=1
                # Stop updating vocaburary if reachs number of sentence
                if num_example == self.num_sents+1:
                    break
                f_vocab.update(self.parse_sentence(f_line))
                e_vocab.update(self.parse_sentence(e_line))
        # Add `NULL` to source vocaburary
        e_vocab.add(self.NULL_TOKEN)
        return e_vocab,f_vocab


def run_expectation_maximization(bitext, config):
    """Implementation of EM for IBM Model 1.

    Args:
      bitext: bitext object for generating sentence pairs.
    Returns:
      ef_prob: conditional probability for p(f|e).
    """
    iteration = config['iteration']

    e_vocab, f_vocab = bitext.build_vocab()
    
    # Init uniform probability
    uniform_prob = 1 / len(f_vocab)

    # Initialize probability with uniform
    ef_prob = {(src_tok, tgt_tok): uniform_prob for src_tok in e_vocab for tgt_tok in f_vocab}
    
    ### CHECK probability of e_i for all f_j###
    # sum_prob = 0 
    # for src_tgt_prob_k in  ef_prob:
    #     if 'of' == src_tgt_prob_k[0]:
    #         sum_prob += ef_prob[src_tgt_prob_k]
    # print('total prob', sum_prob)
    ### CHECK probability of e_i for all f_j###

    for it_step in range(iteration):
        count_src_tgt = defaultdict(lambda: 0)
        count_src = defaultdict(lambda: 0)
        # E-Step
        for sent_pair in bitext.yield_pairs():
            src_sent, tgt_sent = sent_pair
            num_src = len(src_sent)
            num_tgt = len(tgt_sent)
            for i in range(num_tgt):
                denominator_z = 0
                # Compute all alignments
                # Count t( tgt_word_all_j | src_word_i )
                for j in range(num_src):
                    src_word = src_sent[j]
                    tgt_word = tgt_sent[i]
                    k =  (src_word,tgt_word)
                    denominator_z += ef_prob[k]
                # Expected count
                for j in range(num_src):
                    src_word = src_sent[j]
                    tgt_word = tgt_sent[i]
                    k = (src_word,tgt_word)
                    # Normalize
                    c = ef_prob[k] / denominator_z 
                    count_src_tgt[k] += c
                    count_src[src_word] += c
        # M-step
        # Normalize the alignments
        for src_tgt in count_src_tgt:
            src_tgt_expected_count = count_src_tgt[src_tgt] 
            #print(count_src_tgt)
            src_word, _ = src_tgt
            ef_prob[src_tgt] = src_tgt_expected_count / count_src[src_word] 
    return ef_prob

def search_alignment(bitext, prob=None):
    """Create alignment."""
    alignments = list()
    for idx, sent_pair in enumerate(bitext.yield_pairs()):
        # print(idx)
        # print(sent_pair)
        src_sent, tgt_sent = sent_pair
        sentence_alignment = list()
        num_src = len(src_sent)
        num_tgt = len(tgt_sent)
        for i in range(num_tgt):
            best_prob = 0
            best_j = 0
            tgt_word = tgt_sent[i]
            for j in range(num_src):
                src_word = src_sent[j]
                current_prob = prob[(src_word,tgt_word)]
                if current_prob > best_prob:
                    best_prob = current_prob 
                    best_j = j
            # Continue, if j points to `NULL` in f language
            # f_i is not aligned to any word in english sentence
            if best_j == 0:
                continue     

            # Shift one position because of 'NULL'
            sys.stdout.write("%i-%i " % (i, best_j-1))
            src_tgt_align= str(best_j-1) + '-' + str(i) 
            sentence_alignment.append(src_tgt_align)
        #print(sentence_alignment)
        sys.stdout.write("\n")
        alignments.append(sentence_alignment)
    return alignments


def main():
    f_data = "%s.%s" % (args.train, args.french)
    e_data = "%s.%s" % (args.train, args.english)
    
    # Load bitext from `Harsards`
    data = Bitexter(f_data, e_data, int(args.num_sents))
    
    # Run expectation-maximization on list of sentence pairs
    prob = run_expectation_maximization(data, em_config)
    
    # Align sentences from conditional probability 
    alignments = search_alignment(data, prob)
    
if __name__ == '__main__':
    main()



