"""Latent Dirichlet Allocation using Gibbs sampling algorithm.

Note: In the implementation, we uses `z` as topic instead of `z_i` or `t`. 
And `m` for document index. 
"""
import numpy as np
from numpy import asarray, savetxt

import re
import jieba
import codecs
from tqdm import tqdm
from functools import partial

import time
from time import sleep


def preprocessing():
    # 读取停止词文件
    file = codecs.open('./test/stopwords.dic','r','utf-8')
    stopwords = [line.strip() for line in file] 
    file.close()
    
    # 读数据集
    file = codecs.open('./test/dataset_cn.txt','r','utf-8')
    documents = [document.strip() for document in file] 
    file.close()
    
    word2id = {}
    id2word = {}
    docs = []
    currentDocument = []
    currentWordId = 0
    
    for document in documents:
        # 分词
        segList = jieba.cut(document)
        for word in segList: 
            word = word.lower().strip()
            # 单词长度大于1并且不包含数字并且不是停止词
            if len(word) > 1 and not re.search('[0-9]', word) and word not in stopwords:
                if word in word2id:
                    currentDocument.append(word2id[word])
                else:
                    currentDocument.append(currentWordId)
                    word2id[word] = currentWordId
                    id2word[currentWordId] = word
                    currentWordId += 1
        docs.append(currentDocument);
        currentDocument = []
    return docs, word2id, id2word

def doc_generator(docs, return_idx=False):
    idx = 0
    for line in docs:        
        if return_idx:
            yield idx, line
            idx += 1
        else:
            yield line

def load_data(path):
    """Read dataset from path."""
    return open(path, 'r')


def file_generator(path, return_idx=False):
    """Yield sentence or documentline for line"""
    with open(path, 'r') as f:
        idx = 0 
        for line in f:
            line = line.strip().split()
            # line = [1,2,3]
            if return_idx:
                yield idx, line
                idx += 1
            else:
                yield line


class LDA:
    def __init__(self, n_topic, n_doc, vocab_size, alpha=0.1, beta=0.1):
        """Construct Latent Dirichlet Allocation using Gibbs sampling.

        Args:
          n_topic: int, number of topics
          alpha: float, hyperparameter of topic distribution
          beta: float, hyperparameter of word distribution

        Examples:
        >>> import numpy as np
        >>> n_topic = 20
        >>> data = np.array([[13, 1, 0], [3, 2, 0]])
        >>> model = LDA(n_topic)
        >>> model.run()
        """
        self.n_topic = n_topic
        self.alpha = alpha
        self.beta = beta
        self.n_doc = n_doc 
        self.vocab_size = vocab_size

    def initialize(self, line_generator_fn):
        """Initialize count matrix for Gibbs sampling.

        Args:
          line_generator_fn: generator, yields document line
        """
        # doc-word-pair to topic mapping
        # self.topic[(m_idx, w_idx)] = z_idx
        self.topic_dict = dict()
        # 2D-array, number of times document and topic co-ocur
        self.n_mz = np.zeros((self.n_doc, self.n_topic))
        # 2D-array, number of times topic and word co-occur
        self.n_zw = np.zeros((self.n_topic, self.vocab_size))
        # 1D-array, number of documents
        self.n_m = np.zeros(self.n_doc)
        # 1D-array, number of topics
        self.n_z = np.zeros(self.n_topic)

        # m is document index
        for m_idx, m in line_generator_fn(return_idx=True):
            ### Sample z from word at pos i in doc m ###
            # i: word at i position of doc
            # w: word id
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
          m: document index.
          w: word index.

        Gibbs sampler for LDA:
            Left : (num_z_w + beta  ) / (num_z + W * beta  )
            Right: (num_m_z + alpha ) / (num_m + T * alpha )
            propotional: Left * Right
        """
        # Vocab size from document-word matrix
        vocab_size = self.n_zw.shape[1]

        # Perform the propotional terms
        # left: (n_topic, )
        left = ( self.n_zw[:,w] + self.beta) / \
               ( self.n_z + vocab_size * self.beta)
        # right: (, n_topic)
        right = ( self.n_mz[m,:])+ self.alpha / \
                (self.n_m[m] +  self.n_topic * self.alpha)

        # unnormalized z distribution
        z_dist = left * right

        # (n_topic,)
        z_dist /= np.sum(z_dist)
        
        return z_dist

    def run(self, line_generator_fn, iteration=50):
        """Perform training .

        Args:
          line_generator: generator, yields document line
          iteration: running interation for LDA training
        """
        # Initialize parameters
        self.initialize(line_generator_fn)
    
        for it in tqdm(range(iteration)):
            # sleep(0.01)
            for m_idx, m in line_generator_fn(return_idx=True):
                for w_idx, w in enumerate(m):
                    ### Do `except i` ###
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
        
        return None

    def save_file(self, id2word, output_file='out.wid', k=10):
        """Save top-k frequent works to file.

        Args:
          output_file: str, write top k words for each topic
          k: int, number of frequent words to be saved
        """
        # topic-vocab matrix with k words
        # (n_topic, k)
        most_k_zw = self._get_top_k(top_k=k).astype(int)
        # Save 2D integer array without decimal point
        savetxt(output_file, most_k_zw, fmt='%i', delimiter=', ')
        print(f'Saved word indices file to {output_file}')

        with open('out.word', 'w', encoding='utf-8') as wf:
            for most_k in most_k_zw:
                for w_id in most_k:
                    word = id2word[w_id]
                    wf.write(word+' ')    
                wf.write('\n')
            

    def _get_top_k(self, top_k):
        """Search most k frequent words from topic-vocab matrix.

        Returns:
          k_freq_word: 2D array, shape (n_topic, top_k)
        """
        # print('n_zw', self.n_zw)
        # Indices that would sort an array in ascending order
        # Shape (n_topic, vocab_size) 
        r = self.n_zw.argsort(axis=1)
        # (n_topic, top_k)
        k_freq_word = r[:,-top_k:][::-1]
        return k_freq_word # (n_topic, top_k)


# data-t-it-a-b-k

def run_lda():
    return None

def main():
    n_iteration = 50
    n_topic = 10

    file = './test/dataset.txt'

    # parital document generator function 
    # generator, yield index and list of words 
    document_gen_fn = partial(file_generator, path=file)
    
    docs, word2id, id2word = preprocessing()
    document_gen_fn = partial(doc_generator, docs)
    n_doc = len(docs)
    vocab_size = len(word2id)

    # a: 0.02, beta: 0.1
    model = LDA(n_topic=n_topic, n_doc=n_doc, vocab_size=vocab_size,
                alpha=5, beta=0.1)
    
    # Run LDA model using Gibbs sampling
    model.run(document_gen_fn, iteration=n_iteration)

    # Save top k frequent words to file
    model.save_file(id2word, output_file='out.t', k=10)
    
if __name__ == '__main__':
    main()


