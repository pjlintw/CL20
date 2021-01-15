# CL20: Assignment 4

Implementation of the IBM model aligner. We build a IBM model 1 to align English-French setence pairs. We compare the implementation model with other model 1 implementation and higher version IBM model `fast_align` on the hansards parallel sentences.

## Reports

the report is in `/reports/reports.pdf`.

## Setup and Data

1. python version and dependencies 

We uses python 3.7. Before execute file, please install the dependencies:
`pip install -r requirements.txt`

2. prepare data and evaluation script

The implementation utilise sentence files under the `hw2/data/` folder. 
Make sure those files (`hansards.f`, `hansards.a`, `hansards.e`) are included.

We use `score-alignments` for calculating precision, recall and alignment error rate.

### Result Files 

We test the baseline model, our implementation, compare it with another implemenation and IBM model 2 `fast_align` to discuss their performances.
All the file are collected in `results`.

* `results/dice.a`: Evaluating result of baseline model.
* `results/myIBM-#k`: Evaluating result of our IBM model 1.
* `results/dice-#k.a`: Evaluating result of another IBM model 1 implementation. 
* `results/reverse-#k.align`: Evaluating result of `fast_align` .

## Run the aligner

### Basic Usage

Our aligner provides simialr user-interative-command as the baseline aligner
To run our code, you can do: 

```
python run_aligner.py -n 10000 > myIBM-1k
```

The file `myIBM-1k` will have 1000 aligments for each sentence pair:
```
0-9 1-21 2-9 3-9 4-9 5-9 6-9 7-9 8-14 9-8 10-9
0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-4 
...
...
```

### Evaluate the result

To evaluate the result, you should use `score-alignments`. We uses the scripts for all the experiements we have tried.

```
python score-alignments < myIBM-1k
```

### Compare with other Implemenation 

We compare our implementation with other on 1000, 3000 and 500k sentence pairs. It gives similar results between the two implementations.

![alt text](./img/img1.png)


### Compare with `fast_align`

We evaluates our IBM model 1 with the second version of model `fast_align` on different scale datasets. We set the iteration 1 and train them on 10000, 30000, 50000, 80000 sentence pairs. 

Both models perform better when increasing training examples. The `fast_align` can achieve the 28 accuracy with only 1000 examples but our IBM model requires 8x examples. In the recall score, the `fast_align` on 1k, 3k, 5k and 8k are not as good as its precision.   

![alt text](./img/img2.png)


### Visualizations 

We visualize the a aligments example from our implemenation and the baseline. 

Alignments (our)             |  Alignment (other)
:-------------------------:|:-------------------------:
![](./img3-align33-our.png)  |  ![](./img3-align33-baseline.png)
