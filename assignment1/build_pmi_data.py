"""Build bigram and seqment vocabulary."""

import os
import errno
from utils import *

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    handlers=[logging.StreamHandler()]) 

logger = logging.getLogger()


def main():
    # config
    args =get_args()
    config = load_config(args)
    
    # corpus is expected to untokenized sentences
    for path in os.listdir(config['data']['raw_path']):
        path = os.path.join(config['data']['raw_path'], path)
        corpus = load_txt(path, readlines=True)
        logger.info(len(corpus))
        
        # create token-index, index-token dict
        seq_idx = 0

        seq2freq = dict()
        
        seq2idx = dict()
        idx2seq = dict()

        stop_flag = 1
        for line in corpus:
            line_lst = line.strip().split()
            logger.info(line_lst)

            for idx in range(len(line_lst)-1):
                seq_pair = line_lst[idx:idx+2]
                seq_pair = tuple(seq_pair)
                frt_seq, scd_seq = seq_pair


                # count frequency of pair and word
                if seq_pair not in seq2idx:
                    seq2idx[seq_pair] = seq_idx
                    seq2freq[seq_pair] = 1
                    seq_idx += 1
                else:
                    seq2freq[seq_pair] += 1
            

                if frt_seq not in seq2idx:
                    seq2idx[frt_seq] = seq_idx
                    seq2freq[frt_seq] = 1
                    seq_idx += 1
                else:
                    seq2freq[frt_seq] += 1

                if scd_seq not in seq2idx:
                    seq2idx[scd_seq] = seq_idx
                    seq2freq[scd_seq] = 1
                    seq_idx += 1
                else:
                    seq2freq[scd_seq] +=1

            if stop_flag == 10:
                break


            stop_flag += 1

        print(seq2freq)
    # remove word and  word pairs





if __name__ == '__main__':
    main()
