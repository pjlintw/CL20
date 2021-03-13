
# Phrase-Based Translation Model

These implements for the phrased-based translation model allows you to build a phrase table and train a phrase-based translator, to translate the sentence with stack decoding algorithm, and to evalaute the results with BLEU scores. We demonstrate that the phrased-based model obtain the better translation results performed on BELU scores.

A translation model builds on word-by-word transaltion would be a worst translator. We builds a phrase-based translator trained on the **phrase table** and **language model** for the adequacy and the fluency of translated results. 

Note that these phrases need not be linguistically meaningful constituents.

## Features
* Word alignment
* Phrase Table Extraction
* Scoring phrses
* Beams-search
* BLEU score Evaluation

## Files Structure

```
|--data
|  |-- alignments
|  |   |-- IBM1.alignment.it1
|  |   |-- IBM1.alignment.it10
|  |   |-- IBM1.alignment.it20
|  |   └-- IBM1.alignment.it30
|  | 
|  |-- hansards
|  |   |-- hansards.a
|  |   |-- hansards.f
|  |   |-- hansards.e
|  |
|  |-- phease.txt
|  |-- lm.log-prob
|  └-- phrase.log-prob
|

|-- report
|   |-- img
|   |   └---- IMAGE-FOR-REPORT
|   └── reports.pdf
|
|-- results
|-- build_vocab.py
|-- LDA.py
|-- plot_frequency.py
|-- run_analysis.py
|-- run_topk.py
└── README.md
```

## Reports

The report is in `/reports/reports.pdf`.


## Install and Datasets

1. python version and dependencies 

We uses python 3.7. \
To execute the program install the dependencies:
`pip install -r requirements.txt`

2. prepare datasets and word aligmnet file

The implementation uses the sentence files under the `data/hansards/` folder. 
Make sure these files (`hansards.f`, `hansards.a`, `hansards.e`) are included.
#(We use `score-alignments` for calculating precision, recall and alignment error rate.)

Phrased based translation model extracts all possible phrases from the word-to-word alignments \
and tained on these file. We obtained the word aligment files by running our IBM model 1.
You can find these in the `data/alignments/` folder. To reproduce the phrase translation model, 
you don't need to re-run it.

## Build your word alignment file

Your don't need to run this if you just want to train the phrased-based translation model.
The word alignment used for extracting the phrases are included in `data/alignments/` \

To obtain your own word alignment, run the code. 

```
python run_aligner.py --number 100000 \
  --iteration 1 \
  --output data/alignments/IBM1.alignmen.it1 \
  --data_dir PATH_FOR_PARALLEL_SENTENCES \
  --french SOURCE_LANGUAGE_FILE \
  --english TARGET_LANGUAGE_FILE
```

The option `--number` decides number of examples will be used for EM algorithm training. \
`--iteration` specifies number of training iterations. The word-to-word alignment file obtained \
from `--output` will be saved automatically once done with training.

Running the aligner on the other data, you need specify options `--data_dir` for sentence file folder
, `--english` for the target sentence file and `--french` for the source sentence file.

`IBM1.alignmen.it1` stores the French-English aligments (source-target) for the sentence pair.

```
0-9 1-21 2-9 3-9 4-9 5-9 6-9 7-9 8-14 9-8 10-9
0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-4 
...
```

Note that running 100k hansards parallel sentences for one iteration requires **3** minutes.

## Phrased-based Model

We train the translator based on the word alignment files. 

## Train the Phrased-based Translator

The phrased-based model consists of a translation model and a languag model. \
For the translation model, it extracts all the possible phrases as a **phrase translation table** obtained from the word-to-word alignment. The language model estimates the fluency of an sentence in the target language.

The phrase-based model trained to estimate the conditional probability for a sentence in target sentence given a sentence in foreign language. The file will be saved in the folder.

The script estimates log probabilities of p(f|e) of the tranlsation model. To train and save the final conditional probability, you need to pass the word aligment file. 
```
python phrase_translator.py \
  --source_file data/hansards.f \
  --target_file data/hansards/hansards.e \
  --align_file data/alignments/IBM1.alignment.it30 \
  --save_phrase_table data/phrase.txt \
  --output_file data/phrase.log-prob
```

If the command could not found the argument, **Make sure** that you passes the variables to the options correctly.
You will get the result in the command prompt.

```
Saving phrase file to path: data/phrase.txt.
Saving phrase log probability file to path: data/phrase.log-prob.
```

The `phrase.log-prob.` file

```
Saving phrase log probability file to path: data/phrase.log-prob.
```


## Translate the French sentence

Run the code to translate the sentence given input file.

```
python translate.py \
  --input_file \
  --decoding "stack"
  --eval_dir \
  --do_eval
```



## Additional Details

### Evaluation of IBM Model 1 implementation

We compare our implementation with other on 1, 20, 30 and 50 iterations for training EM algorithm in our aligner. We use 100k examples in `hansards` parallel sentences. 







