"""Build bigram and seqment vocabulary. We compute all frequency of terms and seqment pair."""

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
    args =sget_args()
    config = load_config(args)
    
    # frequency threshold
    min_freq = config['data']['min_freq']

    path = os.listdir(config['data']['raw_path'])[0]
    path = os.path.join(config['data']['raw_path'], path)

    # corpus is expected to untokenized sentences
    corpus = load_txt(path, readlines=True)
    
    
    # init dictionary for counting bigram and segment
    num_words = 0
    seg2freq = dict()
    for line in corpus:
        line_lst = line.strip().split()
        logger.info(line_lst)

        # count number of words
        num_words += len(line_lst)
        # count segment frequency
        for segment in line_lst:
            seg2freq = add_count_to_dict(segment, seg2freq)

    # count bigram
    bi2freq = dict()
    for line in corpus:
        line_lst = line.strip().split()
        for idx in range(len(line_lst)-1):
            seg_pair = tuple(line_lst[idx: idx+2])
            first_segment, second_segment = seg_pair

            # continue if one of segments has less than min_freq frequnecy
            first_seg_freq = seg2freq[first_segment]
            second_seg_freq = seg2freq[second_segment]
            if first_seg_freq <= min_freq or second_seg_freq <= min_freq:
                continue
            else:
                bi2freq = add_count_to_dict(seg_pair, bi2freq)

    # dict, bigram pairs to pmi socre
    bigram2pmi = computer_pmi_score(bi2freq, seg2freq, num_words)
    # convert tuple of string to an string
    sorted_dict = { ' '.join(list(k)): v for k, v in sorted(bigram2pmi.items(), key=lambda item: item[1], reverse=True)}

    # dump dict to json
    path = get_processed_dir('pmi_score.json', config)
    dump_dict_to_json(path, sorted_dict)        
        

if __name__ == '__main__':
    main()
