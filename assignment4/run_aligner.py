"""Implementation of IBM model 1 aligner."""
import argparse
from collections import defaultdict

em_config = {'iteration':10000}

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', dest='train', default='hw2/data/hansards')
parser.add_argument('-e', '--english', dest='english', default='e') # target
parser.add_argument('-f', '--french', dest='french' , default='f') # source
parser.add_argument('-n', '--number', dest='num_sents', default=100)
args = parser.parse_args()


class Bitexter:
    def __init__(self, f_data, e_data, num_sents=100):
        self.f_data = f_data
        self.e_data = e_data
        self.num_sents = num_sents
    
    def yield_pairs(self):
        with open(self.f_data, 'r') as f_file, open(self.e_data) as e_file:
            num_example = 0
            for f_sent, e_sent in zip(f_file, e_file):
                num_example +=1
                if num_example == self.num_sents:
                    print('example', num_example)
                    break
                yield self.parse_sentence(f_sent), self.parse_sentence(e_sent)
    
    def parse_sentence(self, sentence):
        return sentence.strip().split()


def em(sentence_generator, config):
    """Implementation of EM for IBM Model 1.

    Args:
      sentence_generator: A list of sentence pairs.
                          `(source_sentence, )`
    Returns:
      alignment: sequence of soruce-target alignment separate by space
    """
    iteration = config['iteration']

    # translation(tgt_word|src_word)
    # `src-tgt` as key
    prob = {'B-X':0.5,
            'B-Y':0.5,
            'C-X':0.5,
            'C-Y':0.5}

    # count_src_tgt = defaultdict(lambda: 0)
    # count_src = defaultdict(lambda: 0)

    for it_step in range(iteration):
        count_src_tgt = defaultdict(lambda: 0)
        count_src = defaultdict(lambda: 0)

        # E-Step
        for sent_pair in sentence_generator:
            src_sent = sent_pair[0].strip().split()
            tgt_sent = sent_pair[1].strip().split()

            num_src = len(src_sent)
            num_tgt = len(tgt_sent)

            # print(sent_pair)
            # print(src_sent, tgt_sent)
            # print(num_src, num_tgt)
            # print(it_step)
            for i in range(num_tgt):
                denominator_z = 0
                # Compute all alignments
                # Count t( tgt_word_all_j | src_word_i )
                for j in range(num_src):
                    src_word = src_sent[i]
                    tgt_word = tgt_sent[j]
                    k =   src_word + '-' + tgt_word  
                    denominator_z += prob[k]
                # Expected count
                for j in range(num_src):
                    src_word = src_sent[i]
                    tgt_word = tgt_sent[j]
                    k = src_word + '-' + tgt_word
            
                    c = prob[k] / denominator_z 
                    count_src_tgt[k] += c
                    count_src[src_word] += c
        # M-step
        # Normalize the alignments
        for src_tgt in count_src_tgt:
            src_tgt_expected_count = count_src_tgt[src_tgt] 
            src_word = src_tgt.split('-')[0]
        
            prob[src_tgt] = src_tgt_expected_count / count_src[src_word] 
        return prob

def search_alignment(sent_pairs, prob=None):
    
    alignments = list()
    for idx, sent_pair in enumerate(sent_pairs):
        sentence_alignment = list()

        src_sent = sent_pair[0].strip().split()
        tgt_sent = sent_pair[1].strip().split()

        num_src = len(src_sent)
        num_tgt = len(tgt_sent)
        # print(src_sent)
        # print(tgt_sent)
        for i in range(num_tgt):
            best_prob = 0
            best_j = 0
            tgt_word = tgt_sent[i]
            for j in range(num_src):
                src_word = src_sent[j]
                current_prob = prob[src_word+'-'+tgt_word]
                if current_prob > best_prob:
                    best_prob = current_prob 
                    best_j = j
            #print('',idx, i, best_j)
            i_j = str(i) + '-' + str(best_j)
            sentence_alignment.append(i_j)
        alignments.append(sentence_alignment)
    return alignments
    
def run_expectation_maximization():
    pass


def main():
    f_data = "%s.%s" % (args.train, args.french)
    e_data = "%s.%s" % (args.train, args.english)

    # sent_pair = ('B C', 'X Y')

    # List of sentence pairs
    sent_pairs = [ ('B C', 'X Y'), ('B', 'Y')]

    data = Bitexter(f_data, e_data, 10)
    prob = em(data, em_config)
    print(prob)
    #aligns = search_alignment(sent_pairs, prob)


if __name__ == '__main__':
    main()



