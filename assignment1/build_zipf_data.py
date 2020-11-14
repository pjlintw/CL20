"""Precessing, build vocabulary and data."""

import os
import errno
from utils import get_args, load_config

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger()


def save_word_freq_from_dict(d, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        {f.write(f'{k} {v}\n') for k,v in d.items()}
        completed_path = os.path.join(os.getcwd(), output_path)
        logger.info('Created file to {}'.format(completed_path))


def get_file_name(path):
    file_path = os.path.splitext(path)
    file_name = file_path[0].split('/')[-1]
    return file_name


def main():
    # config
    args = get_args()
    config = load_config(args)

    # Corpus is expected to untokenized sentences
    token_index = 0
    corpus = list()
    tok2idx = dict()
    tok2freq = dict()
    for path in os.listdir(config['data']['raw_path']):
        path = os.path.join(config['data']['raw_path'], path)
        if not os.path.exists(path):
            logger.info(f"File not exist: {path}")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            corpus.extend(f.readlines())
            for line in corpus:
                if line == '\n':
                    continue
                
                line = line.lower().strip()
                for seg in line.split():
                    if seg not in tok2idx:
                        tok2idx[seg] = token_index
                        token_index += 1
                        tok2freq[seg] = 1
                    else:
                        tok2freq[seg] += 1

            # sort it    
            sortedDict = {k: v for k, v in sorted(tok2freq.items(), key=lambda item: item[1], reverse=True)}
            output_file = get_file_name(path) + '.txt'
            
            # save word frequency file
            save_word_freq_from_dict(sortedDict, output_file)

if __name__ == "__main__":
    main()
