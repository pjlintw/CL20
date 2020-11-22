"""Visulize Zipf's law with line chart."""

import os
from utils import *
import shutil
from pprint import pprint
import matplotlib.pyplot as plt

import re
import numpy as np
import random


def plot_frequency_curve(x_axis, y_axis, _plot_img=None, _title=None):
    """Plot line chart and zipf curve.

    Args:
        x_axis: list of elements on x axis.
        y_axis: list of elements on y axis.
        _plot_img: if given, save the image to the path.
        _title: if given, display it as the title of chart.
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
        fig_title = 'Zipf\'s law: {}'.format(_title)
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

    # load data
    for path in os.listdir(config['data']['processed_path']):
        if path.startswith('.'):
            continue
        # corpus_name 
        print(path)
        file_prefix = get_file_name(path, last_seq=False)
        img_output = 'freq-' + file_prefix + '.jpeg'
        path = get_processed_dir(path, config)
       
        sorted_dict = load_dict_from_json(path)
        word_freq = [ int(v) for k,v in sorted_dict.items() ]
        word_rank = [ i+1 for i in range(len(word_freq)) ]
        
        plot_frequency_curve(x_axis=word_rank, 
                             y_axis=word_freq,
                             _plot_img=img_output,
                             _title=file_prefix)


if __name__ == '__main__':
    main()
