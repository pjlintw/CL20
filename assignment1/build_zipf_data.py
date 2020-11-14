"""Precessing, build vocabulary and data."""

from utils import get_args, load_config


def preprocess(lower_case=False):
    pass


def main():
    # config
    args = get_args()
    config = load_config(args)

    # aceesss config
    corpus_lst = config['vocab']['corpus']
    for corpus_path in corpus_lst:
        print(corpus_path)
        
        # check path is valid
        corpus = list()
        with open(corpus_path, 'r', encoding='utf-8') as f:
            print(repr(f.readlines()))
            corpus.extend(f.readlines())
            print(corpus)



    # preprocess

    # build vocabulary with frequency

    # output
    pass

if __name__ == "__main__":
    main()
