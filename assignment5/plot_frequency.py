"""Plot word frequency of document file."""

from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # doc file
    doc_file = 'data/movies-pp.txt'

    c = Counter()
    with Path(doc_file).open() as f:
        for line in f:
            line = line.strip()
            # Skip first line
            if line == '2000':
                continue
            word_lst = line.split()
            c.update(word_lst)
    
    with open('data/frequent-word.txt', 'w') as f:
        for w, freq in c.most_common():
            f.write(f'{w} {str(freq)}\n')
            
    # Plot
    f, ax = plt.subplots(figsize=(10,5))
    freq_lst = [v for k,v in c.most_common()]
    freq_lst = freq_lst[:300]
    bar = plt.bar(range(len(freq_lst)), freq_lst, color='green', alpha=0.4)

    plt.xlabel('Word Index')
    plt.ylabel('Frequency')
    plt.title('Top 300 Word Frequency')
    plt.legend(loc=2)
    plt.savefig('images/wordFrequency-300.png')








