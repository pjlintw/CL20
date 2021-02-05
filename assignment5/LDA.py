"""Latent Dirichlet Allocation using Gibbs sampling algorithm.

Note: we uses `z` as topic instead of `z_i` or `t`. 
And `m` for document index. 
"""
import os, datetime
import numpy as np
from numpy import asarray, savetxt

import json
import logging
from tqdm import tqdm
from pathlib import Path
from functools import partial

import time
from time import sleep


def create_logger(model_path):
    """Create logger.

    Args: str, path for log file
    """
    logname = os.path.join(model_path, 'main.log')
    Path('results').mkdir(exist_ok=True)
    logging.basicConfig(filename=logname,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    logging.info("Running LDA")
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)

    return logger


def file_generator(path, return_idx=False):
    """Yield sentence or documentline for line"""
    with open(path, 'r') as f:
        idx = 0 
        for line in f:
            line = line.strip().split()
            
            if return_idx:
                yield idx, line
                idx += 1
            else:
                yield line


class LDA:
    def __init__(self, n_topic, doc_path, vocab_path, model_path, logger, alpha=0.02, beta=0.1):
        """Construct Latent Dirichlet Allocation using Gibbs sampling.

        Args:
          n_topic: int, number of topics
          doc_path: str, 
          vocab_path: str,
          alpha: float, hyperparameter of topic distribution
          beta: float, hyperparameter of word distribution

        Examples:
        >>> import numpy as np
        >>> n_topic = 20
        >>> data = np.array([[13, 1, 0], [3, 2, 0]])
        >>> model = LDA(n_topic)
        >>> model.run(input_fn, iteration=50, save_per_iteration=100)
        """
        self.n_topic = n_topic
        self.alpha = alpha
        self.beta = beta
        self.logger = logger

        # Count number of documents
        with Path(doc_path).open() as f:
            self.n_doc = sum( 1 for _ in f) 
        
        # Count vocabulary and mapping dicts
        with Path(vocab_path).open() as f:
            self.word2id = { w.strip():i for i, w in enumerate(f)} 
        
        self.id2word = dict((v,k) for k,v in self.word2id.items())
        self.vocab_size = len(self.id2word)

        # Create model folder
        self.model_path = model_path
 

    def _initialize(self, input_fn):
        """Initialize count matrix for Gibbs sampling.

        Args:
          input_fn: generator, yields list or word.
        """
        # doc-word-pair to topic mapping
        # self.topic[(m_idx, w_idx)] = z_idx
        self.topic_dict = dict()
        # 2D-array, number of times document and topic co-ocur
        self.n_mz = np.zeros((self.n_doc, self.n_topic))
        # 2D-array, number of times topic and word co-occur
        self.n_zw = np.zeros((self.n_topic, self.vocab_size))
        # 1D-array, number of topics is assigned to document
        self.n_m = np.zeros(self.n_doc)
        # 1D-array, number of words is assigned to topic
        self.n_z = np.zeros(self.n_topic)

        # m is document (list or word ids)
        for m_idx, m in input_fn(return_idx=True):
            # Map word into id
            m = [self.word2id[w] for w in m]
            
            ### Sample z from word at pos i in doc m ###
            # w_idx: word at i position of doc
            # w    : word id
            for w_idx, w in enumerate(m):
                z = np.random.randint(self.n_topic)
                self.topic_dict[(m_idx , w_idx)] = z 
                self.n_mz[m_idx, z] += 1              
                self.n_m[m_idx] += 1     
                self.n_zw[z, w] +=1 
                self.n_z[z] += 1
        print('Initialize paramters...')

    
    def _sample_from_multinomial(self, dist):
        """Sample a corresponding index from given distribution."""
        return np.random.multinomial(1, dist).argmax()


    def _gibbs_sampling(self, m, w):
        """Update p(z_i | z_not_i, w) using gibbs sampling.

        Args:
          m: int, document index.
          w: int, word index.

        Gibbs sampler for LDA:
            Left : (num_z_w + beta  ) / (num_z + W * beta  )
            Right: (num_m_z + alpha ) / (num_m + T * alpha )
            propotional: Left * Right
        """
        # Vocab size from document-word matrix
        # vocab_size = self.n_zw.shape[1]

        # Perform the propotional terms
        # Left: (n_topic, ) + scalar /
        #       (n_topic, ) + scalar * scalar
        left = ( self.n_zw[:,w] + self.beta) / \
               ( self.n_z       + self.vocab_size * self.beta)

        # Right: (n_topic, ) + scalar /
        #        scalar      + scalar * scalar
        right = (self.n_mz[m,:] + self.alpha) / \
                (self.n_m[m]    + self.n_topic * self.alpha)

        # Unnormalized z distribution
        # (n_topic, ) * (n_topic, )
        z_dist = left * right

        # Normalize. (n_topic,)
        z_dist /= np.sum(z_dist)
    
        return z_dist

    def run(self, input_fn, iteration=50, save_per_iteration=None):
        """Perform training.

        Args:
          input_fn: generator, it yields document per line
          iteration: int, running interation for LDA training
        """
        # Initialize parameters
        self._initialize(input_fn)

        # Run Gibbs sampling 
        for it in tqdm(range(iteration)):
            for m_idx, m in input_fn(return_idx=True):
                # Map word into id
                m = [self.word2id[w] for w in m]
                
                for w_idx, w in enumerate(m):
                    ### Do `except at i position` ###
                    z = self.topic_dict[(m_idx, w_idx)]
                    self.n_mz[m_idx, z] -= 1              
                    self.n_m[m_idx] -= 1     
                    self.n_zw[z,w] -=1 
                    self.n_z[z] -= 1

                    # Estimate topic distribution
                    # Shape (n_topic, )
                    z_distribution = self._gibbs_sampling(m=m_idx, w=w)

                    # Sample from multinomial 
                    z = self._sample_from_multinomial(z_distribution)
                    self.topic_dict[(m_idx, w_idx)] = z
                    self.n_mz[m_idx, z] += 1              
                    self.n_m[m_idx] += 1     
                    self.n_zw[z,w] +=1 
                    self.n_z[z] += 1

            # Save model per iteration
            if save_per_iteration is not None and (it+1) % save_per_iteration == 0:
                ### topic-word matrix: zw ###
                # Add None to axis 1 for broadcasting
                # `zw_logit`: (n_topic, vocab_size) + scalar /
                #             (n_topic, None      ) + scalar * scalar
                # (n_topic, vocab_size)
                zw_logit = ( self.n_zw + self.beta) / \
                           ( self.n_z[:,None] + self.vocab_size * self.beta)
                
                # zw_distribution: (n_topic, vocab_size) /
                #                  (COLUMN-WISE-SUM, None) 
                # (n_topic, vocab_size)
                zw_distribution = zw_logit / \
                                  np.sum(zw_logit, axis=1)[:,None] 

                ### document-topic matrix: mz ###
                # mz_logit: (n_doc, n_topic) + scalar /
                #           (n_doc, None   ) + scalar * scalar
                # (n_doc, n_topic)
                mz_logit = (self.n_mz + self.alpha) / \
                           (self.n_m[:,None] +  self.n_topic * self.alpha)
                # mz_distribution: (n_doc, n_topic) /
                #                  (COLUMN-WISE-SUM, None)             
                mz_distribution = mz_logit / \
                                  np.sum(mz_logit, axis=1)[:,None]
                
                # Save zw npz
                output_file = os.path.join(self.model_path, f'zw-iteration{it+1}.npz')
                np.savez(output_file, zw_distribution)
                self.logger.info('Saved model: {}'.format(f'zw-iteration{it+1}.npz'))

                # Save mz npz
                output_file = os.path.join(self.model_path, f'mz-iteration{it+1}.npz')
                np.savez(output_file, mz_distribution)
                self.logger.info('Saved model: {}'.format(f'mz-iteration{it+1}.npz'))


        
    def save_file(self, output_file='word.word', k=10):
        """Save top-k frequent works to file.

        Args:
          output_file: str, write top k words for each topic
          k: int, number of frequent words to be saved
        """
        # topic-vocab matrix with k words
        # (n_topic, k)
        k_word_idx, k_word_logit = self._get_top_k(top_k=k)
        
        with Path(os.path.join(self.model_path, output_file)).open('w', encoding='utf-8') as wf: 
            for row_idx, most_k in enumerate(k_word_idx):
                for col_idx, w_id in enumerate(most_k):
                    word = self.id2word[w_id]
                    word_score = k_word_logit[row_idx, col_idx]
                    wf.write('{} {},'.format(word, word_score))
                wf.write('\n')
            

    def _get_top_k(self, top_k):
        """Search most k frequent words from topic-vocab matrix.
        
        Args:
          top_k: K most frequent words to be selected
        
        Returns:
          k_word_idx: 2D array, shape (n_topic, top_k), indies of k words.
          k_word_logit: 2D array, shape (n_topic, top_k), logits of k words.
        
        Examples:

        >>> k = 2
        >>> self.n_zw
        # row-wise index
        #  0   1  2
        [[10,  8, 1],
         [32, 11,20]]

        >>> k_word_idx, k_word_logit = self._get_top_k(k)
        >>> k_word_idx
        [[0, 1],
         [0, 2]]

        >>> k_word_logit
        [[10, 8],
         [32,20]]
        """
        # Indices that would sort an array in ascending order
        # Shape (n_topic, vocab_size) 
        indices_mat = self.n_zw.argsort(axis=1)

        # Slicing last k columns, reverse columns (n_topic, top_k)
        k_word_idx = indices_mat[:,-top_k:][:, ::-1]

        # K word socre in `n_zw` matrix (n_topic, top_k)
        k_word_logit = np.take_along_axis(self.n_zw, k_word_idx, axis=1)
        return k_word_idx, k_word_logit  # both are (n_topic, top_k)


def main():
    # Params
    params = {
        'alpha': 0.02,
        'beta': 0.1,
        'n_iteration': 500,
        'n_topic': 20,
        'top_k': 10,
        'save_per_iteration': 100,
        'doc_path': 'data/movies-pp-20.txt', 
        'vocab_path': 'data/vocab.txt',     
        'model_path': 'results'  # all files will be savied here
    }

    # Create result folder
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    params['model_path'] = os.path.join(params['model_path'], now_time)
    Path(params['model_path']).mkdir(parents=True, exist_ok=True)

    # Save params
    with Path(os.path.join(params['model_path'], 'params.json')).open('w') as f:
        json.dump(params, f, indent=4, sort_keys=True)


    # Create logger
    logger = create_logger(params['model_path'])


    # alpha: 0.02, beta: 0.1
    model = LDA(n_topic=params['n_topic'],
                doc_path=params['doc_path'],
                vocab_path=params['vocab_path'],
                model_path=params['model_path'],
                alpha=params['alpha'],
                beta=params['beta'],
                logger=logger)
    
        
    # Document generator function (callback)
    # yields list of word ids and index if `return_idx` True 
    document_gen_fn = partial(file_generator, path=params['doc_path'])
    
    
    # Run LDA model using Gibbs sampling
    model.run(input_fn=document_gen_fn,
              iteration=params['n_iteration'],
              save_per_iteration=params['save_per_iteration']) # save .npz file


    # Save top k frequent words to file
    model.save_file(output_file='out.word', k=params['top_k'])


    
if __name__ == '__main__':
    main()


