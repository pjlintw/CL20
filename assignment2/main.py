
from hmm import HiddenMarkovModel

import numpy as np

i_matrix = np.array([0.6, 0.2, 0.2])
e_matrix = np.array([[0.7,0, 0.3],
                     [0.1,0.9,0],
                     [0, 0.2,0.8]])

print(i_matrix.shape)
print(e_matrix.shape)
print(np.dot(e_matrix, i_matrix))


def viterbi_searching(observation,
                     initial_probability,
                     transition_probability,
                     emission_probability):
    """Implement Viterbi algorithm.
    
    Args:
      observation
      initial_probability
      transition_probability
      emission_probability
    Return:
      state_seq: list, sequence of states
    """
    pass
    

def main():
    pass

if __name__ == '__main__':
    main()
