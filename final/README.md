# Phrase-Based Translation Model

[Datasets](#datasets) | [Phrased-based Model](#phrased-based-model) | [Translatte with Stack Decoder](#translate-with-stack-decoder)

These implements for the phrased-based translation model allows you to build a phrase table and train a phrase-based translator, to translate the sentence with stack decoding algorithm. We demonstrate that the phrased-based model obtain the good and readable translation results.

A translation model builds on word-by-word transaltion would be a worst translator. We builds a phrase-based translator trained on the **phrase table** and **language model** for the adequacy and the fluency of translated results. 

Note that these phrases need not be linguistically meaningful constituents.

## Features

This repository implements these features for statistical machine translation.

* Word Alignment
* Phrase Table Extraction
* Stack Decoder


## Files Structure

There are many files in this repository. The figure below explains the purpose of these files. Note that `#N` refers to an number with the file. For example, `phrase-maxlen#N.txt` means a phrase file with maximal length `#N`.

```
|--data
|  |-- alignments
|  |   |-- IBM1.alignment.it1   # word alignment runing 1 iteration obtained by `run_aligner.py.py`
|  |   |-- IBM1.alignment.it10
|  |   |-- IBM1.alignment.it20
|  |   └-- IBM1.alignment.it30
|  | 
|  |-- hansards                
|  |   |-- hansards.f            # 100k sentences in French 
|  |   |-- hansards.e            # 100k sentences in English 
|  |   |-- hansards-300.f        # 300 french sentence to translate
|  |   └-- test.sentences        # 48 french sentence to translate
|  |
|  |-- phease-maxlen#N.txt       # phrase file
|  |-- phrase-manlen#N.log-prob  # log-probabilities for phrase 
|  |-- lm                        # log-probabilities for LM
|  └-- tm                        # log-probabilities for phrase
|
|-- report
|   |-- img
|   |   └---- IMAGE-FOR-REPORT
|   └── report.pdf              # Report 
|
|-- result                            
|   |-- hansards-300.stack3.maxlen3.t # translation on Hansards with stack size #N and phrase length #N
|   |-- test.stack#N.maxlen#N.t       # translation given 48 sentences with stack size #N and phrase length #N

|   └── reports.pdf
|
|-- requirements.txt
|-- models.py                   # Class for phrase model and language model
|-- phrase_translator.py        # Implementation of phrase extraction and phrase model
|-- stack_decoding.py           # Implementation of stack decoder
└── README.md
```


Note that the files in `hansards` folder are nessary for training phrase model and to translate. The files are **not offering**. Please collect them by following steps in `datasets` section. 

## Reports

The report is in `/reports/report.pdf`.


## Install

we use python 3.7 and dependencies in `requirements.txt` 
Check you python version is:

* python 3.7

Install the dependencies by run the code in thecommand prompt:

`pip install -r requirements.txt`

## Datasets

The implementation uses the French-English sentence files under the `data/hansards/` folder. Make sure these files `hansards.f`, `hansards.e` are included. You need to download them via the Github repository: [link](https://github.com/xutaima/jhu-mt-hw/tree/master/hw2/data).

It's also important that we evaluate the stack decoder on two French sentence files `hansards-300.f` and `test.sentences`. These files are not offering too. 
Once you download  `hansards.f` and `hansards.e` in the `data/hansards/`. Extract first 300 sentences in `handsards.f` and wirte it as the `hansards-300.f` file. We need it for evaluating the performance of phrase-to-phrase translation.

In addition, we use another French sentences to evaluate our phrase translation model.
The file `test.sentences` contains 48 French sentences from a public data in the  
 [link](https://github.com/xutaima/jhu-mt-hw/tree/master/hw3/data). Please download the `input` file in link and rename it as `test.sentences`.
 
All the files mentions above are **necessary** for runing (1) word alignment, (2) phrase translation model, and (3) stack decoder. Please check these files are in `data/hansards/` and the arguments for input files are correct once you re-run the codes.

`lm` and `tm` files refer to log-probabilities for phrase translation model and language model. In our experiments, we only exvaluate our log-probabiliies for phrase translation file `phrase-manlen#N.log-prob`. You will need `lm` for the stack decoder, please download `lm` file from the [link](https://github.com/xutaima/jhu-mt-hw/tree/master/hw3/data)



The phrased-based translation model extracts all possible phrases from the word-to-word alignments and tained on these file. We obtained the word aligment files by running our IBM model 1. You can find these in the `data/alignments/` folder. To reproduce the phrase translation model, you don't need to re-run it.

## Build your word alignment file

Your don't need to run this if you just want to train the phrased-based translation model. The word alignment used for extracting the phrases are included in `data/alignments/` 

If you need run your alignments. To obtain it, run the code. 

```
python run_aligner.py --number 100000 \
  --iteration 30 \
  --output data/alignments/IBM1.alignmen.it1 \
  --data_dir PATH_FOR_PARALLEL_SENTENCES \
  --french SOURCE_LANGUAGE_FILE \
  --english TARGET_LANGUAGE_FILE
```

The option `--number` decides number of examples will be used for EM algorithm training. 
`--iteration` specifies number of training iterations. The word-to-word alignment file obtained from `--output` will be saved automatically once done with training.

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

The phrase-based model extracts all possible phrase based on the word alignments. We first extracts the phrases and estimate the log-probability of phrases. Then translate the French sentences using beam-search decoder.

The complete translation process consists of (1) **phrase translation model** and (2) **stack decoder**. The details of running these programs can be found in the two following section.

We refer the phrase translation model as the log-probability of phrase.

## Train the Phrased-based Translator

The translation process consists of a phrase translation model and a languag model. For the translation model, it extracts all the possible phrases as a **phrase translation table** obtained from the word-to-word alignment. The language model estimates the fluency of an sentence in the target language.

The phrase-based model is designed to estimate the conditional probability for a phrase in source language given another phrase in target language. The formula **P(f | e)** is derived from noisy-channels model.

The script estimates log probabilities of **P(f | e)** of the tranlsation model. To train and save the final conditional probability, you need to pass the word aligment file. 

The following script uses an example fpr extracting phrases with maximal phrase length 3. It will create `phrase-maxlen3.log-prob` for the log-probabilisties of phrases and a file `phrase-maxlen3.txt ` with phrases along. If set `max_phrase_len` 0, there is no limit for maximal phrase length.

```
python phrase_translator.py \
  --source_file data/hansards/hansards.f \
  --target_file data/hansards/hansards.e \
  --align_file data/alignments/IBM1.alignment.it30 \
  --save_phrase_table data/phrase-maxlen3.txt \
  --output_file data/phrase-maxlen3.log-prob \
  --max_phrase_len 3
```

The runtime is taking 27 seconds for extracting 2781789 phrases on 10k sentences according the alignments. On average, it costs 0.00028 seconds per sentence.


If the command could not found the argument, **make sure** that you use the arguments correctly. You will get the result in the command prompt.


```
Maximal phrase length 3.
Extracting phrases for 5000 sentences...
Extracting phrases for 10000 sentences...
Extracting phrases for 15000 sentences...
Extracting phrases for 20000 sentences...
Extracting phrases for 25000 sentences...
Extracting phrases for 30000 sentences...
Extracting phrases for 35000 sentences...
Extracting phrases for 40000 sentences...
Extracting phrases for 45000 sentences...
Extracting phrases for 50000 sentences...
Extracting phrases for 55000 sentences...
Extracting phrases for 60000 sentences...
Extracting phrases for 65000 sentences...
Extracting phrases for 70000 sentences...
Extracting phrases for 75000 sentences...
Extracting phrases for 80000 sentences...
Extracting phrases for 85000 sentences...
Extracting phrases for 90000 sentences...
Extracting phrases for 95000 sentences...
Extracting phrases for 100000 sentences...
Running 27.9119 seconds for 100000 sentences.
0.00028 seconds per sentence.
Saving phrase file to path: data/phrase-maxlen3.txt.
Extract 2781789 phrases.
Saving phrase log probability file to path: data/phrase-maxlen3.log-prob.
```


The `phrase-maxlen3.log-prob` file is the phrase translation model: 

```
et les consultations ||| and consultations ||| -0.6931471805599453
et de consultations ||| and consultations ||| -1.3862943611198906
et plusieurs consultations ||| and consultations ||| -1.3862943611198906
```


## Translate with Stack Decoder

It's important that we evaluate the stack decoder on two French sentences files `hansards-300.f` and `test.sentences`. We are not offering these files. Please create the files by the instructions in the `Datasets` section above.


download these from the Github repository: [link](https://github.com/xutaima/jhu-mt-hw). 


For the translation, we implement a **stack decoder** to translate the English sentences given French sentences and to evaluate the capacity of **phrase-to-phrase** translation built on the phrase count of Hansards datasets. First, we evaluate the phrase translation model on 300 French sentences, `hansards-300.f`, derived from Handsards datasets. In addition, we also evlaute it on another 48 French sentences in the `test.sentences`, where . It offered by the machine transaltion lecture in Johns hopkins University. 

Run the code to translate the sentence given input file.

The example runs the stack decoder on `hansards-300.f` file using the phrase translation model `phrase-maxlen3.log-prob` with stack size 3 . The translation reults `hansards-300.maxlen3.t` will saved in the `result` folder.

```
python stack_decoding.py \
  --input data/hansards/hansards-300.f \
  --translation_model data/phrase-maxlen3.log-prob \
  --stack_size 3 \
  --write_file result/hansards-300.stack3.maxlen3.t
```

Runing the example is taking Running 6.0170 seconds for 300 sentences.
0.02006 seconds per sentence. The runtime will increase when using longer stack size. 

With stack size 15 for the same setting, it runs 28.3204 seconds and 0.09440 seconds per sentence.

## Additional Details

### Evaluation of IBM Model 1 implementation

We compare our implementation with other on 1, 20, 30 and 50 iterations for training EM algorithm in our aligner. We use 100k examples in `hansards` parallel sentences. 

