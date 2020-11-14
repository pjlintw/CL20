"""Visulize Zipf's law with line chart."""

from utils import get_args, load_config
import shutil
from pprint import pprint
import matplotlib.pyplot as plt

import random

def plot_wcc_distribution(xdist, ydist, _plot_img='x.jpeg'):
    """Plot weakly connected components size distributions
    :param _g: Transaction graph
    :param _plot_img: WCC size distribution image (log-log plot)
    :return:
    """

    plt.figure(figsize=(14, 12))
    plt.clf()
    plt.loglog(xdist, ydist, 'ro-')
    plt.title("Zipf's Law")
    plt.xlabel("Rank")
    plt.ylabel("Word Frequency")
    plt.savefig(_plot_img)
    
    print("saved image in {}".format(_plot_img))

def main():
    # get config
    args = get_args()
    config = load_config(args)
    pprint(config)

    rng = random.Random(123)
    # save config

    # tokenize

    # count freqency

    # visualize
    x = [i+1 for i in range(100)]
    y = [rng.randint(1, 100) for _ in range(100)]
    plot_wcc_distribution(x,y)

if __name__ == '__main__':
    main()

