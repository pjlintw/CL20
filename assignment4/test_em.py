"""Test em on examplei."""
from collections import defaultdict

em_config = {'iteration':100}

def em(sent_pair, config):
    """Implementation of EM for IBM Model 1.

    Args:
      sent_pair: a pair of source and target sentence
    Returns:
      alignment: sequence of soruce-target alignment separate by space
    """
    iteration = config['iteration']

    sent_pair = ('B C', 'X Y')
    src_sent = sent_pair[0].strip().split()
    tgt_sent = sent_pair[1].strip().split()

    num_src = len(src_sent)
    num_tgt = len(tgt_sent)

    # translation(tgt_word|src_word)
    prob = {'B-X':0.2,
            'B-Y':0.5,
            'C-X':0.5,
            'C-Y':0.5}

    count_tgt_src = defaultdict(lambda: 0)
    count_src = defaultdict(lambda: 0)
    for it_step in range(iteration):
        for i in range(num_src):
            denominator_z = 0

            # Compute all alignments
            for j in range(num_tgt):
                src_word = src_sent[i]
                tgt_word = tgt_sent[j]
                
                # Count t( tgt_word_all_j | src_word_i )
                k =   src_word + '-' + tgt_word  
                denominator_z += prob[k]
                
                
            # Normalize the alignments

            for j in range(num_tgt):
                src_word = src_sent[i]
                tgt_word = tgt_sent[j]
                k =   src_word + '-' + tgt_word
                prob_tgt_given_src = prob[k]

                c = prob_tgt_given_src/denominator_z 
                count_tgt_src[k] += c
                count_src[src_word] += c

        
        for src_tgt in count_tgt_src:
            src_tgt_expected_count = count_tgt_src[src_tgt] 
            src_word = src_tgt.split('-')[0]
            
            src_expected_count = count_src[src_word] 
            prob[src_tgt] = src_tgt_expected_count / src_expected_count
        print(prob)

def main():
    sent_pair = ('B C', 'X Y')

    em(sent_pair, em_config)
    
if __name__ == '__main__':
    main()



