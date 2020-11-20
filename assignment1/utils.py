"""Implement utilities."""

import os
import time
import yaml
import argparse
from pathlib import Path


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


def save_word_freq_from_dict(d, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        { f.write("{}, {}\n".format(k,v)) for k,v in d.items()}
        completed_path = os.path.join(os.getcwd(), output_path)
        print("created file to {}".format(completed_path))


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
