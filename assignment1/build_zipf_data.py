"build vocabulary and its frequency."""

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

    # corpus is expected to untokenized sentences
    for path in os.listdir(config['data']['raw_path']):
        # check path
        if path.startswith('.'):
            continue
        path = os.path.join(config['data']['raw_path'], path)
        if not os.path.exists(path):
            logger.info(f"File not exist: {path}")
            continue
        elif not os.path.isfile(path):
            logger.info(f"Skip. path is a directory: {path}")
            continue

        # init dict for word-frquency mapping
        tok2freq = dict()
        words = 0
        corpus = load_txt(path, readlines=True)
        for line in corpus:
            if line == '\n':
                continue                
            line = line.lower().strip()
            words += len(line.split())
            # line = line.translate(str.maketrans('','', string.punctuation))
            for seg in line.split():
                if seg not in tok2freq:
                    tok2freq[seg] = 1
                else:
                    tok2freq[seg] += 1
        print('words in totel', path, words)
        # sorting by descending order
        sorted_dict = {k: v for k, v in sorted(tok2freq.items(), key=lambda item: item[1], reverse=True)}
        output_file = 'src-' + get_file_name(path) + '.json'
        output_file = get_processed_dir(output_file, config)

        # dump dict to json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, indent=1, ensure_ascii=False)
            logger.info('dump word-frequency dictionary to : {}'.format(output_file))


if __name__ == "__main__":
    main()
