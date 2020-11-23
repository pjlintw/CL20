"""Traina ngram and generating sequence."""

import os
import errno
import random
from utils import *
from models.ngram import BasicNgram

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    handlers=[logging.StreamHandler()]) 

logger = logging.getLogger()

SEP = '[SEP]'

def main():
    # config
    args = get_args()
    config = load_config(args)

    # get parameters
    num_step = config['data']['num_step']
    context_size_lst = config['data']['context_size']
    random_seed = config['seed']

    # random object
    rdn = random.Random(random_seed)

    # load data 
    # corpus: ['3', '+', '2', '=', '5', '\n', ...]
    file_name = 'arithmetic-10000.train'
    path = get_raw_dir(file_name, config)
    corpus = load_txt(path, readlines=True)   

    # flatten the list and add special tokens
    # ngram_corpus: ['[SEP]', '3', '+', '2' = '5', '[SEP]', ...]
    ngram_corpus = list()
    for line in corpus:
        line_lst = [SEP] + line.strip().split() 
        ngram_corpus.extend(line_lst) 
        
    len_corpus = len(ngram_corpus)

    # train 2, 3, 4, 5-gram here
    for context_size in context_size_lst:
        ngram_model = BasicNgram(context_size, ngram_corpus)
        result_collection = list()

        # random choice start token
        # context_tup: ('tok', 'tok', ...)
        start_idx = rdn.choice(range(len_corpus))
        context_lst = ngram_corpus[start_idx: start_idx+context_size-1]
        context_tup = tuple(context_lst)

        # ensure length of context equal n - 1
        assert len(context_tup) == (context_size -1)
        
        result_collection.extend(context_lst)
        
        # generate sequence
        for _ in range(num_step-len(context_lst)):
            generated_tok = ngram_model[(context_tup)].generate()

            result_collection.append(generated_tok)
            start_idx = - (context_size-1)
            context_tup = tuple(result_collection[start_idx:]) 

            # ensure length of context equal n - 1
            assert len(context_tup) == (context_size -1)
            
        # write result
        output_path = get_processed_dir('result-{}gram.o'.format({context_size}), config)
        with open(output_path, 'w', encoding='utf-8') as f:
            for idx in range(len(result_collection)):
                current_token = result_collection[idx]
                if current_token == '[SEP]':
                    f.write('[SEP]\n')
                else:
                    f.write('{} '.format(current_token))
                
                
if __name__ == '__main__':
    main()









