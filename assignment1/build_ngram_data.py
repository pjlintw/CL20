"""Genenerate arithmetic problems for ngram model."""

import random
from utils import *


def main():
    # config
    args = get_args()
    config = load_config(args)
    
    # set parameters
    rdn = random.Random(config['seed'])
    num_question = 10000
    num_test = 100
    total_ammount = num_question + num_test
    train_file_path = get_raw_dir('arithmetic-10000.train', config)
    test_file_path =  get_raw_dir('arithmetic-100.test', config)
    
    question_lst = list()
    for _ in range(total_ammount):

        # random sample two digits
        big_num = rdn.randint(0, 99)
        first_digit = rdn.randint(0, big_num)
        
        # if True creating adddtion question, otherwise substraction 
        doPlus = bool(rdn.randint(0, 1))
        if doPlus:
            second_digit = big_num - first_digit
            line = '{} + {} = {}\n'.format(first_digit, second_digit, big_num)
            question_lst.append(line)
        else:
            second_digit = big_num - first_digit
            line = '{} - {} = {}\n'.format(big_num, first_digit, second_digit)
            question_lst.append(line)
    
    train_lst = question_lst[:num_question]
    test_lst = question_lst[-num_test:]

    with open(train_file_path, 'w', encoding='utf-8') as f:
        f.write(''.join(train_lst))
    
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(''.join(train_lst))


if __name__ == '__main__':
    main()
