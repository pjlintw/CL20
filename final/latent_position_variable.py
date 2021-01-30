"""Context vector

p(x, y) = p(y|x)p(x)

p(y)
x --f-> y' --g--> x'


p(x) = p(w_3|w_2) * p(w_2|w_1) * p(w_1)

len = 5
[ [0, 1, 2, 3, 4],
  [0, 1, 2, 1, 4],
  [0, 1, 2, 3, 4]] 

wp: (vocab_size+[sos], max_len-1)

        pos0  pos1 pos2 pos3 (pos4)
[sos]    3     0    0    0     0
w1       0     3    0    1     0
w2       0     0    3    0     0
w3       0     0    0    2     0
([eos])  0     0    0    0     5




-> h (n_position, 1)

pw: (max_len-1, vocab_size +[ens])

        w1  w2   w3   [eos]
pos0    3   0    0     0
pos1    0   3    0     0 
pos2    1   0    2     0
pos3    0   0    0     3

w1   = [0,3,0,1,0]
pos3 = [1,0,2,0,0]

pw_transpose w2_hidden
    (w,h) (h, 1)
[3,0,1,0] * [0
[0,3,0,0]    0
[1,0,2,0]    3
[0,0,0,3]    0]

out 
  (w,1)
[3] -> w1
[0]
[6] -> w3
[0]


pw_transpose w1_hidden
[3,0,1,0] * [0
[0,3,0,0]    3
[1,0,2,0]    0
[0,0,0,3]    1]

out 
[0] 
[9] -> w2
[0]
[3]


pw_transpose w1+w2_hidden
[3,0,1,0] * [0
[0,3,0,0]    0
[1,0,2,0]    6
[0,0,0,3]    0]

out 
[6] 
[0] -> w2
[12]
[0]

pw_transpose w1+w2+w3_hidden
[3,0,1,0] * [0
[0,3,0,0]    4
[1,0,2,0]    0
[0,0,0,3]    2]

out 
[0] 
[12] -> w2
[0]
[6]


pw_transpose w1+__+w3_hidden
[3,0,1,0] * [0
[0,3,0,0]    3
[1,0,2,0]    0
[0,0,0,3]    3]

out 
[0] 
[9] -> w2
[0]
[9]
"""
import numpy as np


class PositionLanguageModel:
    def __init__(self, vocab_size, max_len):
        self.vocab_size = vocab_size
        self.max_len = max_len
        

    def _initialize(self):
        # number of time word is assigned to position
        self.n_wp = np.zeros((vocab_size-1, max_len-1))
        # number of time position is assigned to word
        self.n_pw = np.zeros((max_len-1, vocab_size-1))
        # print(self.n_wp.shape)
        # print(self.n_pw.shape)
        return None
    

    def fit(self, sentents):
        self._initialize()

        BOS_ID = 0
        EOS_ID = 4
        for sent in sentents:
            for idx, word_id in enumerate(sent):
                # Update position distribution
                if idx != len(sent)-1:
                    self.n_wp[word_id, idx] += 1

                # Update word distribution
                if idx != len(sent)-1:
                    word_id = sent[idx+1]-1
                    self.n_pw[idx, word_id] += 1
        # # Normalize
        self.wp_distribution = self.n_wp / np.sum(self.n_wp, axis=1)[:,None]
        self.pw_distribution = self.n_pw / np.sum(self.n_pw, axis=1)[:,None]

    def get_prob(self, sent):
        """Compute probability."""
        hidden = self.wp_distribution.take(sent, axis=0)        
       
        print(hidden.T)
        print(self.pw_distribution)
        # (word, 1)
        o = np.matmul(self.pw_distribution, hidden.T)
        return hidden, o 


# Create dataset
sentents = np.array([[0,1,2,3,4],
                     [0,1,2,1,4],
                     [0,1,2,3,4]])


# Params
max_len = 5
# include [sos] [eos]
vocab_size = 5 
model = PositionLanguageModel(vocab_size=vocab_size, max_len=max_len)

# Train
model.fit(sentents)

h, o = model.get_prob([2])

print(h.T.shape)
print(o)

# # Output        
# print(model.wp_distribution)
# print(model.pw_distribution)

# # # p(w_t | w_t-1)
# # w1 at any positions
# context_matrix = np.array([[0, 0, 0,0],[0,0.75,0,0.25],[0,0,0,0], [0,0,0,0]])

# context_vector = np.array([0,0,1, 0])[:,None]

# print('shape', context_vector.shape)
# print('shape', context_matrix.shape)

# w_dist = np.matmul(pw_distribution, context_vector)
# print(w_dist)





"""
positive_content(y)


cycleGAN for baysian
p(y|x) ~= p(x|y)p(y)

langaugePrior(y) = score
x -> p(x) -> y -> p(y) -> x 

I love moive -> Ich habe Hunger -> hi hi hi

enc(pos) = h_j
enc(neg) = h_i


c(h) -> [0-1]

p(x, y) = p(y|x)p(x)

I hate watching   movie
|   |     |          |
I  love watching  moive

p(x,y) = p(y|x) = p(x|y)p(y)
     
      p(x_char|y)p(y)

       word1 word2 word3
word1 [                 ]
word2 [                 ]
word3 [                 ]

p(word3|word1, word2) = weight_decay * p(w3|w2) * p(w3|w2)
"""



