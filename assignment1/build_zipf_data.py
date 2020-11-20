"Precessing, build vocabulary and data."""

import os
import errno
from utils import *

import json
import string
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def main():
    # config
    args = get_args()
    config = load_config(args)

    # Corpus is expected to untokenized sentences
    for path in os.listdir(config['data']['raw_path']):
        if path.startswith('.'):
            continue
        path = os.path.join(config['data']['raw_path'], path)
        if not os.path.exists(path):
            logger.info(f"File not exist: {path}")
            continue
        elif not os.path.isfile(path):
            logger.info(f"Skip. path is a directory: {path}")
            continue

        # init container, token-index mapping
        token_index = 0
        corpus = list()
        tok2idx = dict()
        tok2freq = dict()
        # read file as a list of sentences
        print('read file ', path)
        corpus = load_txt(path, readlines=True)
        # logger.info(len(corpus))
        for line in corpus:
            if line == '\n':
                continue                
            line = line.lower().strip()
            # line = line.translate(str.maketrans('','', string.punctuation))
            for seg in line.split():
                if seg not in tok2idx:
                    tok2idx[seg] = token_index
                    token_index += 1
                    tok2freq[seg] = 1
                else:
                    tok2freq[seg] += 1

        # sort it    
        sorted_dict = {k: v for k, v in sorted(tok2freq.items(), key=lambda item: item[1], reverse=True)}
        output_file = 'src-' + get_file_name(path) + '.json'
        output_file = get_processed_dir(output_file, config)

        logger.info(output_file)
        # dump dict to json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
