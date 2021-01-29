"""Using the normalised topic-word matrix as word representations."""

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
    # Indices matrix
    most_sim_word_indices = cos_sim_arr.argsort()[-k:][::-1]
    # Map index into word
    k_word_lst = [ id2word[w_idx] for w_idx in  most_sim_word_indices]
    
    # Get cosine similarity score by index
    score_arr = cos_sim_arr.take(most_sim_word_indices)
    
    # pair of word-score list
    # (k,). Each element is (word, score)
    k_word_score_lst = list(zip(k_word_lst, score_arr))
    return k_word_score_lst


def print_most_k_word(k_word_score_lst, baseline_word, top_k):
    """List the similar k words."""
    print('Baseline word: {}'.format(baseline_word))
    for i in range(top_k):
        w, cos_sim = k_word_score_lst[i]
        s = f'{w:>10} {cos_sim:.5}'
        print('{} most similar word:'.format(i+1), s)


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
    # Result folder
    result_folder = 'results/2021-01-25_01-00-15'

    # Load mapping dict
    vocab_file = 'data/vocab.txt' 
    word2id, id2word = load_vocab(vocab_file)
    vocab_size = len(word2id)

    # Load topic word matrix
    np_file = 'zw-iteration500.npz'
    zw = np.load(Path(result_folder,np_file))['arr_0']

    # Get list of cosine similarity score
    baseline_word = 'film'
    compare_words = ['film', 'movie', 'video', 'cinema', 'theater', 
                     'hospital', 'nurse', 'patient', 'thief',
                     'actress', 'casting']
    
    compare_lst = compare_similarity(baseline_word=baseline_word, 
                                    compare_word_lst=compare_words, 
                                    zw_matrix=zw, 
                                    score_fn=cosine_similarity,
                                    word2id=word2id,
                                    id2word=id2word)
    joint_str = ', '.join(compare_words)
    print(f'Similarity between `{baseline_word}` and \n`{joint_str}`')
    for i in range(len(compare_words)):
        w, cos_sim = compare_lst[i]
        s = f'{w:>10} {cos_sim:.5}'
        print('{} most similar word:'.format(i+1), s)
    print()



    # Get list of cosine similarity score
    baseline_word = 'julia'
    compare_words = ['james', 'bond', 'tarantino', 'john', 'stanley', 
                     'hospital', 'nurse', 'patient', 'thief',
                     'actress', 'casting']
    
    compare_lst = compare_similarity(baseline_word=baseline_word, 
                                    compare_word_lst=compare_words, 
                                    zw_matrix=zw, 
                                    score_fn=cosine_similarity,
                                    word2id=word2id,
                                    id2word=id2word)
    joint_str = ', '.join(compare_words)
    print(f'Similarity between `{baseline_word}` and \n`{joint_str}`')
    for i in range(len(compare_words)):
        w, cos_sim = compare_lst[i]
        s = f'{w:>10} {cos_sim:.5}'
        print('{} most similar word:'.format(i+1), s)
    print()



    # `film`, 'happy', 'vampir', 'comedy', 'killer'
    # Get k most similar words by cosine similarity
    baseline_word = 'killer'
    top_k = 10
    k_word_score_lst = get_most_similar_k_word(baseline_word=baseline_word, 
                                               k=top_k, 
                                               zw_matrix=zw, 
                                               score_fn=cosine_similarity,
                                               word2id=word2id,
                                               id2word=id2word)
    print_most_k_word(k_word_score_lst, baseline_word, top_k=top_k)
    print()


    # Get k most similar words by cosine similarity
    baseline_word = 'crime'
    top_k = 10
    k_word_score_lst = get_most_similar_k_word(baseline_word=baseline_word, 
                                               k=top_k, 
                                               zw_matrix=zw, 
                                               score_fn=cosine_similarity,
                                               word2id=word2id,
                                               id2word=id2word)
    print_most_k_word(k_word_score_lst, baseline_word, top_k=top_k)









