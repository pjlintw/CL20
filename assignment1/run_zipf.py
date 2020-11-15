"""Visulize Zipf's law with line chart."""

import os
from utils import get_args, load_config, get_processed_dir, get_file_name
import shutil
from pprint import pprint
import matplotlib.pyplot as plt

import random

def plot_frequency_curve(x_axis, y_axis, _plot_img):
    """Plot weakly connected components size distributions
    :param _g: Transaction graph
    :param _plot_img: WCC size distribution image (log-log plot)
    :return:
    """
    # fig = plt.figure(figsize=(14, 12))
    fig, ax1 = plt.subplots(figsize=(14,12))

    ax1.semilogy(x_axis, y_axis)
    ax1.set(title='semilogy')
    ax1.grid()

    plt.title("Zipf's Law")
    plt.xlabel("Rank")
    plt.ylabel("Word Frequency")

    fig.tight_layout()
    plt.savefig(_plot_img)
    print("saved image in {}".format(_plot_img))


def main():
    # get config
    args = get_args()
    config = load_config(args)
    pprint(config)

    rng = random.Random(123)
    # save config

    # load data
    for path in os.listdir(config['data']['processed_path']):
        # corpus_name 
        file_prefix = get_file_name(path, last_seq=True)
        img_output = 'freq-' + file_prefix + '.jpeg'
        print(img_output)
        # img_output = ''.join('freq-', path.split('-')[1:])
        path = get_processed_dir(path ,config)
        word_rank = list()
        word_freq = list()
        with open(path, 'r', encoding='utf-8') as f:    
            l = 0
            for line in f.readlines():
                line = line.strip()
                word, freq = line.split()
                
                #print(type(word))
                #print('freq', type(freq))
                word_rank.append(word)
                word_freq.append(freq)
                
                l += 1
                if l == 50:
                    break

        print(len(word_rank))
        print(len(word_freq))
        word_rank = [ i+1 for i in range(len(word_freq,), 0, -1)]
        
        plot_frequency_curve(x_axis=word_freq, 
                             y_axis=word_rank,
                             _plot_img=img_output)


if __name__ == '__main__':
    main()
