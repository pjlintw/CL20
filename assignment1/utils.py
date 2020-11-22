"""Implement utilities."""

import os
import json
import time
import yaml
import argparse
import json
import numpy as np
from pathlib import Path

def computer_pmi_score(bi2feq, seg2freq, num_words):
    """Compute pmi score.

    Implement pmi approximation:
        pmi(w1, w2) ~= log ((count(w1,w2) * num_words) / count(w1) * count(w2))

    Args:
        bi2freq: dictionary, mapping bigram pair to frequency
        seg2freq: dictionary, mapping segment to frequency
        num_words: number of words in the corpus
    Retrun:
        bi2pmi: dictionary, tuple of two segments and its pmi socre
    """
    bi2pmi = dict()

    for each_bigram in bi2feq:
        # unpack tuple of tow segments
        first_segment, second_segment = each_bigram
        first_seg_freq, second_seg_freq = seg2freq[first_segment], seg2freq[second_segment]
        denominator = first_seg_freq * second_seg_freq

        bigram_freq = bi2feq[each_bigram]
        pmi_score = np.log((bigram_freq*num_words) / denominator)

        bi2pmi[each_bigram] = pmi_score

    return bi2pmi


def get_args():
    """Get Parser."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--config", type=str, default="config.yml")

    return parser.parse_args()


def load_config(args):
    """Load configuration ifle."""
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


def load_txt(path, readlines=False):
    with open(path, 'r', encoding='utf-8') as f:
        if readlines:
            corpus = f.readlines()
        else:
            corpus = f.read() 
    return corpus


def load_dict_from_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

    
def dump_dict_to_json(path, dump_dict):
    # dump dict to json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(dump_dict, f, indent=1, ensure_ascii=False)
        print('dump dictionary to : {}'.format(path))


def save_word_freq_from_dict(d, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        { f.write("{}, {}\n".format(k,v)) for k,v in d.items()}
        completed_path = os.path.join(os.getcwd(), output_path)
        print("created file to {}".format(completed_path))


def add_count_to_dict(item, item2freq):
    """Count frequency of item in dictionary.

    Args:
        item: key in dictionay
        item2freq: dictionary object
    Return:
        item2freq: dictionary that stores item-frequency
    """

    if item not in item2freq:
        item2freq[item] = 1
    else:
        item2freq[item] += 1
    return item2freq


def get_file_name(path, last_seq=False):
    """Strip repositories and file extension.

    Args:
      path: file path.
      last_seq: if true, return the last seqment of file name.
    """
    file_path = os.path.splitext(path)
    file_name = file_path[0].split('/')[-1]

    if last_seq:
        return file_name.split('-')[-1]
    return file_name


def get_raw_dir(path, config):
    raw_dir = config['data']['raw_path']
    if not os.path.isdir(raw_dir):
        os.makedirs(raw_dir)
    return os.path.join(os.getcwd(), raw_dir, path)


def get_processed_dir(path, config):
    processed_dir = config['data']['processed_path']
    if not os.path.isdir(processed_dir):
        os.makedirs(processed_dir)
    return os.path.join(os.getcwd(), processed_dir, path)


def timeit(method):
    """Measuring execution time of method.
    ```python
    
    >>>@timeit
    >>>def add(x, y):
           return x + y
    
    >>>f(5, 10)
    f: 0.00095367431640625
    ```

    Args:
        method: callable method
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        ti_dif = (te - ts) * 1000
        print('{}: {:.4f} ms'.format(method.__name__, (ti_dif)))

        return result

    return timed

def create_dir(path):
    """Savely creating recursive directories"""
    if not isinstance(path, Path):
        path = Path(path)

    if not os.path.exists(path):
        os.makedirs(path)
        print('Created directory: {}'.format(path))
    else:
        print('Directory {} already exists.'.format(path))
