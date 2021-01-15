"""Build 1k, 3k, 5k, 8k, 10k data for fast align"""
import os

def main():
    data_repo = 'hw2/data/'
    size_lst = [1000, 3000, 5000 , 80000, 10000]
    
    file_str = 'align-data-{}k'

    f_data = os.path.join(data_repo, 'hansards.f')
    e_data = os.path.join(data_repo, 'hansards.e')
    sen_collect = list()
    with open(e_data) as e_file, open(f_data) as f_file:
        n = 0
        for e_line, f_line in zip(e_file, f_file):
            if n+1 == size_lst[-1]:
                break
            n += 1
            e_line = e_line.strip()
            f_line = f_line.strip()
            sen_collect.append(e_line+' ||| '+f_line)

    for each_size in size_lst:
        size_str = str(each_size)[0] if each_size!=10000 else '10'
        with open(file_str.format(size_str), 'w') as f:
            f.write('\n'.join(sen_collect[:each_size]))

if __name__ == '__main__':
    main()
