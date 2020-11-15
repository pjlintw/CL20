"""Visulize Zipf's law with line chart."""

import os
from utils import get_args, load_config, get_processed_dir, get_file_name
import shutil
from pprint import pprint
import matplotlib.pyplot as plt

import re
import numpy as np
import random


def plot_frequency_curve(x_axis, y_axis, _plot_img=None, _title=None):
    """Plot weakly connected components size distributions
    :param _g: Transaction graph
    :param _plot_img: WCC size distribution image (log-log plot)
    :return:
    """
    
    fig, axs = plt.subplots(2, 1, figsize=(14, 12))

    axs[0].plot(x_axis, y_axis)
    axs[0].set_ylabel('word frequency', fontsize=14, fontweight='bold')
    axs[0].grid(True)

    axs[1].loglog(x_axis, y_axis)
    axs[1].set_xlabel('rank', fontsize=14, fontweight='bold')
    axs[1].set_ylabel('word frequency', fontsize=14, fontweight='bold')
    axs[1].grid(True)

    if _title is not None:
        fig_title = f'Zipf\'s law: {_title}'
    else:
        fig_title = 'Zipf\s law'
    
    fig.suptitle(fig_title, fontsize=20, fontweight='bold')

    if _plot_img is not None:
        plt.savefig(_plot_img)
        print("saved image in {}".format(_plot_img))


def main():
    # get config
    args = get_args()
    config = load_config(args)

    # save config

    # load data
    for path in os.listdir(config['data']['processed_path']):
        # corpus_name 
        file_prefix = get_file_name(path, last_seq=True)
        img_output = 'freq-' + file_prefix + '.jpeg'
        # img_output = ''.join('freq-', path.split('-')[1:])
        path = get_processed_dir(path ,config)
        word_rank = list()
        word_freq = list()
        with open(path, 'r', encoding='utf-8') as f:    
            for line in f.readlines():
                line = line.strip()
                word, freq = line.split()
                freq = int(freq)                
                word_freq.append(freq)
                
        word_rank = [ i+1 for i in range(len(word_freq))]
        plot_frequency_curve(x_axis=word_rank, 
                             y_axis=word_freq,
                             _plot_img=img_output,
                             _title=file_prefix)


if __name__ == '__main__':
    main()
