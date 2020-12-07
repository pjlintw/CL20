# CL20: Assignment 2


## Reports

the report is in `/reports/reports.pdf`

## Reproducing the result

1. python version and dependencies 

We uses python 3.7. Before execute file, please install the dependencies:
`pip install -r requirements.txt`

2. additional `models/ngram.py` for unknown word

We use ngram model for replacing unknown word. Please use the script `ngram.py` in assignment 1 and 
under a `models` folder from the importing in `main.py` .

## Data

The model uses annotated German datases `de-utb` and it's laoded by `ConllCorpusReader`. Make sure the training set is a CoNLL format file. The training, evaluation and test sets were under `de-utb` folder.

## Run HMM tagger

### Configurate various HMM tagger for unknown words 

We contruct a `HiddenMarkovTagger` class, which allow you to tranin and evaluate Bigram-based HMM tagger on CoNLL datasets.
The tagger estimates an optimal sequence of tags by using Viterbi algorithm `_viterbi_searching()`.  The model uses 
`de-utb/de-train.tt` for traning, evaluate its performance on file `de-utb/de-test.t`. Configurate the repository if you are
not using the same dataset.
  
`HiddenMarkovTagger` provides various mechanisms to deal with unknown words while inference. The HMM(bigram), which is baseline, uses bigram model
to replace the unknown word by predicting the missing one in vocabulary given previous word. The HMM(bigram+randomFirstToken) tries to improve the unknown 
word at first position by random sampling first words from all first words in training sets. The third one HMM(sampleDistribution) simply replaces all 
unknown word by sampling from word distribution of the training sets. (It showns better performance but it's extremly slow.). Finally, MM(empirical) follows empirical rule
of unknown word, which **usually** are `NOUN`. We replace all unknown words by a word whose tag is `NOUN`.

You can execute various HMMtagger by adjusting the parameters of `HiddenMarkovTagger` (Line 335 in main.py). Please assign the boolean flags to the parameters
`use_bigram`, `sample_from_distribution` and `random_first_token` correctly as the table below.

To use different functions for unknown word, pass `bool` to the parameters of the class. **Notice that: `random_first_token` will be used when `use_bigram` is `True`.**
```
hmm_tagger = HiddenMarkovTagger(data_dir=DATADIR,
                                train_file=train_file,
                                eval_file=test_file,
                                use_bigram=False,
                                sample_from_distribution=False, 
                                random_first_token=False)
```

### Train and Evaluate:

`python main.py`

# Results

| models | use bigram | random first token | sample from distribution | speed (sec.) | accuracy |
| ------ | ---------- | ------------------ | ------------------------ | ------------ | -------- |
| HMM(bigram) | `True` | `False` | `False` | slow (8.7685) | 0.8411 |
| HMM(bigram+randomFirstToken) | `True` | `True` | `False` | slow (9.3351) | 0.8513 |
| HMM(sampleDistribution) | `False` | `False` | `True` | extremly slow (18.4848) | 0.8707 |
| HMM(empirical) | `False` | `False` | `False` | **fast (6.8549)** | **0.8714** |
