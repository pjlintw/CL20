
"""

positive_content(y)


cycleGAN for baysian
p(y|x) ~= p(x|y)p(y)

langaugePrior(y) = score
x -> p(x) -> y -> p(y) -> x 

I love moive -> Ich habe Hunger -> hi hi hi

enc(pos) = h_j
enc(neg) = h_i


c(h) -> [0-1]

p(x, y) = p(y|x)p(x)

I hate watching   movie
|   |     |          |
I  love watching  moive

p(x,y) = p(y|x) = p(x|y)p(y)
     
      p(x_char|y)p(y)

       word1 word2 word3
word1 [                 ]
word2 [                 ]
word3 [                 ]

p(word3|word1, word2) = weight_decay * p(w3|w2) * p(w3|w2)
"""
import numpy as np
from numpy import dot
from numpy.linalg import norm
from pathlib import Path

from pprint import pprint
from functools import partial


def load_vocab(file):
    """Load vocabulary from file."""
    with Path(file).open() as f:
        word2id = dict([ (w.strip(),i) for i, w in enumerate(f)])
    id2word = { v:k for k,v in word2id.items()}
    return word2id, id2word


def get_k_label(zw_matrix, id2word, k=1):
    """Get k labels from highest probability."""
    n_row, n_col = zw.shape

    z = zw_matrix
    print(z.sum(axis=1))


def cosine_similarity(v1, v2):
    """Compute cosine similarity between two vectors."""
    cos_sim = dot(v1, v2) / (norm(v1)*norm(v2))
    return cos_sim


def get_most_similar_k_word(baseline_word, k, zw_matrix, score_fn, word2id, id2word):
    """Find most similar k words."""    
    baseline_idx = word2id[baseline_word]
    cos_sim_fn = partial(cosine_similarity, v1=zw_matrix[:,baseline_idx])

    vocab_size = len(word2id)
    cos_sim_arr = np.zeros((vocab_size))

    for col_idx in range(vocab_size):
        v2 = zw[:, col_idx]
        score = cos_sim_fn(v2=v2)
        cos_sim_arr[col_idx] = score   
    #
    most_sim_word_indices = cos_sim_arr.argsort()[-k:][::-1]
    # Map index into word
    k_word_lst = [ id2word[w_idx] for w_idx in  most_sim_word_indices]
    
    # Get cosine similarity score by index
    score_arr = cos_sim_arr.take(most_sim_word_indices)
    
    # pair of word-score list
    # (k,). Each element is (word, score)
    k_word_score_lst = list(zip(k_word_lst, score_arr))
    return k_word_score_lst


def compare_similarity(baseline_word, compare_word_lst, zw_matrix, score_fn, word2id, id2word):
    """Compute similarity score given a list of words.

    Returns:
      compare_lst: list, a list of word and score pair.

    Example:
      [(word1, 0.23),(word, 0.32), (word, 0.6)]
    """
    # Mapping word into index
    compare_indices = [ word2id[w] for w in compare_word_lst]

    # Get baseline vector
    baseline_idx = word2id[baseline_word]
    baseline_vector = zw[:,baseline_idx]

    # Collect words and its score
    compare_lst = list()
    for idx, w_idx in enumerate(compare_indices):
        second_vector = zw[:,w_idx]

        compare_word = compare_word_lst[idx]
        cos_sim_score = cosine_similarity(baseline_vector, second_vector)
        compare_lst.append((compare_word, cos_sim_score))
    return compare_lst


if __name__ == '__main__':
    
    # # Load mapping dict
    # word2id, id2word = load_vocab('vocab.txt')
    # vocab_size = len(word2id)

    # # Load topic word matrix
    # np_file = 'zw-iteration500.npz'
    # zw = np.load(np_file)['arr_0']



    # # Get list of cosine similarity score
    # baseline_word = 'film'
    # compare_words = ['film', 'movie', 'video', 'cinema', 'theater', 
    #                  'hospital', 'nurse', 'patient', 'thief',
    #                  'actress', 'casting']
    
    # compare_lst = compare_similarity(baseline_word=baseline_word, 
    #                                 compare_word_lst=compare_words, 
    #                                 zw_matrix=zw, 
    #                                 score_fn=cosine_similarity,
    #                                 word2id=word2id,
    #                                 id2word=id2word)
    # print(f'Similarity between `{baseline_word}`')
    # print(compare_lst)

    # # print(get_k_label(zw, id2word, k=1))

    

    # # Get k most similar words by cosine similarity
    # baseline_word = 'film'
    # k_word_score_lst = get_most_similar_k_word(baseline_word=baseline_word, 
    #                                            k=5, 
    #                                            zw_matrix=zw, 
    #                                            score_fn=cosine_similarity,
    #                                            word2id=word2id,
    #                                            id2word=id2word)
    # print(k_word_score_lst)

    for _ in range(5):
        Path('randomFold/se').mkdir(parents=True, exist_ok=True)






