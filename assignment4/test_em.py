"""Test em on examplei."""
from collections import defaultdict

em_config = {'iteration':10000}

def em(sent_pair, config):
    """Implementation of EM for IBM Model 1.

    Args:
      sent_pair: a pair of source and target sentence
    Returns:
      alignment: sequence of soruce-target alignment separate by space
    """
    iteration = config['iteration']

    # List of sentence pairs
    sent_pairs = [ ('B C', 'X Y'), ('B', 'Y')]

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
        for sent_pair in sent_pairs:
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
        print(prob)

def main():
    sent_pair = ('B C', 'X Y')

    em(sent_pair, em_config)
    
if __name__ == '__main__':
    main()



