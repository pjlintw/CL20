# CL20: Assignment 1 


## Reports

the report is in `/reports/reports.pdf`

## Configuration and Reproducing

To execute python file, you should add argument `--config config_{assignment name}.yml` in command line. All configurations are provided in the config files. Follow the steps of each sections.

Before execute file, please install the dependencies:
`pip install -r requirements.txt`

## Data

File name should be distinguish since the file extension will be removed for creating new JSON file. You should manuelly add ".txt" in the end of file if your files are distinguish by extention,  like `SETIMES.bg-tr.tr` and `SETIMES.bg-tr.bg`. 

## Zipf's Law   

### Step 1. Build zipf's law data

`python build_zipf_data.py --config config-zipf.yml`

the data will be saved under `/datasets/zipf/proceesed/` repository.

### Step 2. Run zipf's law charts

`python run_zipf.py --config config-zipf.yml`

# N-gram

### Step 1. Build ngram data

`python build_ngram_data.py --config config-gram.yml`

the data will be saved under `/datasets/ngram/proceesed/` repository.

### Step 2. Run ngram model

`python run_ngram.py --config config-ngram.yml.`


# Statistical Dependence

### Step 1. run pmi

`python run_pmi.py --config config-pmi.yml`



