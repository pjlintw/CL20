
from hmm import HiddenMarkovModel

import numpy as np

from nltk.corpus.reader import ConllCorpusReader

DATADIR = 'de-utb'
train_file = 'de-train.tt'


###  test decoding ###
# transition probability
# A = np.array([[0.8, 0.1, 0.1], 
#               [0.2, 0.7, 0.1], 
#               [0.1, 0.3, 0.6]])

# # initial probability
# C = np.array([0.6, 0.2, 0.2])

# # emission probability
# B = np.array([[0.7, 0.0, 0.3], 
#               [0.1, 0.9, 0.0], 
#               [0.0, 0.2, 0.8]])


# O = np.array([0, 2, 0, 2, 2, 1]).astype(np.int32)

    
# a, b, c= viterbi_searching(O, C, A, B)
# print(a, b, c, sep='\n')
###  test decoding ###

def viterbi_searching(observation,
                      init_dist,
                      transition_matrix,
                      emission_matrix):
    """Implement Viterbi algorithm.
    
    Args:
      observation: sequence of observation with shape 
      init_dist:
      transition_probability:
      emission_probability
    Return:
      state_seq: list, sequence of states
    """
    num_state = transition_matrix.shape[0]
    seq_len = len(observation)

    # Initialize accumulated prob matrix
    accu_prob = np.zeros((num_state, seq_len))
    backpointer = np.zeros((num_state, seq_len-1))

    # state in first position 
    accu_prob[:, 0] = np.multiply(init_dist, emission_matrix[:, 0])

    # update each entry of accumulated probability matrix
    for seq_idx in range(1, seq_len):
        for state_idx in range(num_state):
            # prob of current state i from previous states
            temp_product = np.multiply(transition_matrix[:, state_idx], accu_prob[:, seq_idx-1])
            accu_prob[state_idx, seq_idx] = np.max(temp_product) * emission_matrix[state_idx, O[seq_idx]]
            backpointer[state_idx, seq_idx-1] = np.argmax(temp_product)

    # backtracking
    opt_seq = np.zeros(seq_len).astype(np.int32)
    opt_seq[-1] = np.argmax(accu_prob[:, -1])
    for n in range(seq_len-2, 0, -1):
        opt_seq[n] = backpointer[int(opt_seq[n+1]), n]

    return opt_seq, accu_prob, backpointer
    


def main():
    # file
    conllReader = ConllCorpusReader(DATADIR, train_file, columntypes=('words', 'pos'))
    
    # for i in f.tagged_sents():
    #     print(i)


if __name__ == '__main__':
    main()
