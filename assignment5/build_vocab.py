"""Build word vocab."""

__author__ = 'Pin-Jie Lin'

from collections import Counter
from pathlib import Path

if __name__ == '__main__':
    # Document file
    doc_file = './movies-pp.txt'
    
    # Count frequency
    counter_word = Counter()
    with Path(doc_file).open() as f:
        for line in f:
            counter_word.update(line.strip().split())
    
    # Write file
    with Path('vocab.txt').open('w') as f:
        for w, c in counter_word.most_common():
            f.write('{}\n'.format(w))
