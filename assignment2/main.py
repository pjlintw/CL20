import time
import numpy as np
import random
from collections import Counter
from nltk.corpus.reader import ConllCorpusReader
from models.ngram import BasicNgram
import os

np.set_printoptions(formatter={'float': "{: 7.4f}".format})

class HiddenMarkovTagger:
    def __init__(self,
                 data_dir, 
                 train_file,
                 eval_file=None,
                 use_bigram=False,
                 sample_from_distribution=False,
                 sample_first_tok=False):
        """Implement Hidden Markov Tagger.

        Args:
          data_dir: folder of dataset.
          train_file: path to training data.
          eval_file: path to eval. If given, the model will test on it.
          use_bigram: whether uses bigram to replace unknown word.
          use_sample: sample sample for corpus distribution
          replace_first_tok: if first token is unknown, random sample first token
        """
        self.data_dir = data_dir
        self.train_file = train_file
        self.eval_file = eval_file
        self.conllReader = ConllCorpusReader(data_dir, train_file, columntypes=('words', 'pos'))
        self.tagged_sents = self.conllReader.tagged_sents()
        self.sents = self.conllReader.sents()
        self.use_bigram = use_bigram
        self.sample_from_distribution = sample_from_distribution
        self.sample_first_tok = sample_first_tok
        
    def train(self, do_eval=False, output_file='o.txt'):
        """Calculate the initial, transition and emission probability.

        Args:
          do_eval: if true, evaluate HMM on the data of `eval_file`.
          output_file: file to write.
        """
        s = time.time()
        self.init_probs, self.transition_probs, self.emission_probs = self._build()
        run_time_str = str(round(time.time()-2, 2))
        #print('Taking {} for traning'.format(run_time_str))

        # bigram smoothing
        if self.use_bigram:
            self.bigram = self._build_bigram()

        if self.sample_first_tok:
            self.rdn = random.Random(50)

        # if true, do evalute
        if do_eval:
            self._evaluate(eval_path=self.eval_file, output_file=output_file)

    def _build_bigram(self):
        """Build bigram."""
        ngram_corpus = list()
        [ ngram_corpus.extend(['[SOS]'] + sent) for sent in self.conllReader.sents()]
        bigram = BasicNgram(2, ngram_corpus)
        return bigram

    def _build(self):
        """ Create init probs, transition probs, emission probs. 
        # 
        # init probs      : num_state_i_at_idx_0  / num_sents
        # transition probs: num_state_i2j         / num_state_i
        # emission probs  : num_state_token_ij    / num_state_i
        """
        # count number of tags, tokens and sentences
        self.tags = { pair[1]:0  for sent in self.tagged_sents for pair in sent}
        self.tokens = {pair[0]:0 for sent in self.tagged_sents for pair in sent}
        self.num_tag = len(self.tags)
        self.num_tok = len(self.tokens) 
        self.num_sents = len(self.conllReader.sents())   

        # add `[SOS]` if use_bigram to predict next token
        if self.use_bigram:
            self.tokens['[SOS]'] = 0
            self.num_tok += 1

        # Create token-index, tag-index mapping and its invert dict
        self.tag2idx = { t: idx for idx, t in enumerate(self.tags) }
        self.idx2tag = { idx: t for t, idx in self.tag2idx.items() }
        self.tok2idx = { w: idx for idx, w in enumerate(self.tokens)}
        self.idx2tok = { idx: w for w, idx in self.tok2idx.items()}

        # Init Counters
        first_tags = [sent[0][1] for sent in self.tagged_sents]
        self.firstTag2freq = Counter(first_tags)
        self.tok2freq = Counter()
        self.tag2freq = Counter()
        self.pair2freq = Counter()
        self.tokTag2freq = Counter()

        # `ConllCorpusReader`.tagged_sents() yields lists of tuple
        # [('Der', 'DET'), ('Hauptgang', 'NOUN'), ..., ('.', '.')]
        for tagged_sent in self.conllReader.tagged_sents():
            # group into a pair of sequence and tags
            # [(A,1), (B, 2), (C, 3)] -> (A,B,C), (1,2,3)
            sent, _tags = zip(*tagged_sent)
            transition_pairs = list(zip(_tags, _tags[1:]))
            # count frequencies
            self.tokTag2freq.update(tagged_sent)
            self.tok2freq.update(sent)
            self.tag2freq.update(_tags)
            self.pair2freq.update(transition_pairs)

        # Create token distribution
        self.tok_dis_arr = np.zeros((self.num_tok,))
        for tok in self.tok2freq:
            tok_idx = self.tok2idx[tok]
            self.tok_dis_arr[tok_idx] = self.tok2freq[tok]
        self.tok_dis_arr = self.tok_dis_arr / self.tok_dis_arr.sum()

        init_probs = self._create_init_probs()
        transition_probs = self._create_transition_probs()
        emission_probs = self._create_emission_probs()
        return init_probs, transition_probs, emission_probs

    def _create_init_probs(self):
        """Create initial probability.
            
        Formula: 
            init_prob = num_state_i_at_idx_0 / num_sents
        """
        print('Creating initial probability')
        init_probs = np.zeros((self.num_tag))
        for idx in range(self.num_tag):
            tag = self.idx2tag[idx]
            first_tag_freq = self.firstTag2freq[tag]
            init_probs[idx] = first_tag_freq / self.num_sents
        print('initial probability has shape: {}'.format(init_probs.shape) )
        return init_probs

    def _create_transition_probs(self):
        """Create transition probability. 

        Transition matrix with shape (num_tag, num_tag). For each transition i to j, the
        formula without smoothing is:
            transition_ij =  (num_state_ij + 1) / (num_state_i + |NumTag|)
        """ 
        print('Creating transition probability')
        transition_matrix = np.ones((self.num_tag, self.num_tag))
        for i in range(self.num_tag):
            for j in range(self.num_tag):
                cur_tag = self.idx2tag[i]
                next_tag = self.idx2tag[j]
                try:
                    num_state_ij = self.pair2freq[(cur_tag, next_tag)]
                except:
                    num_state_ij = 0
                num_state_i = self.tag2freq[cur_tag]
                smoothed_num_state_i = num_state_i + self.num_tag
                trans_prob = (transition_matrix[i,j] + num_state_ij) / smoothed_num_state_i
                transition_matrix[i,j] = trans_prob
        print('transition probability has shape: {}'.format(transition_matrix.shape))
        return transition_matrix

    def _create_emission_probs(self):
        """Create emission probability.
         
        Emission matrix with shape (num_tag, num_tok). For each tag i and token k, the formula
        without smoothing:
            emission_ik = (num_tag_i_tok_k + 1) / (num_state_i + |NumTag|*|NumToken|)
        """
        emission_matrix = np.ones((self.num_tag, self.num_tok))
        for i in range(self.num_tag):
            for k in range(self.num_tok):
                cur_tag = self.idx2tag[i]
                tok = self.idx2tok[k]
                try:
                    num_tag_i_tok_k = self.tokTag2freq[(tok, cur_tag)]
                except:
                    num_tag_i_tok_k = 0
                num_state_i = self.tag2freq[cur_tag]
                smoothed_num_state_i = num_state_i + (self.num_tag * self.num_tok)
                emission_matrix[i,k] = (emission_matrix[i,k]+ num_tag_i_tok_k) / smoothed_num_state_i
        print('emission probability has shape: {}'.format(emission_matrix.shape))
        return emission_matrix

    def tag(self, observation):
        """Estimate sequence of tags.

        Args:
          observation: list of tokens, tokenized sentence.
        Retruns::
          estimated_tags: list of tags.
        """
        # ['Guten', 'Tag', '!'] -> [3, 5, 11]
        seq_id = self.encode(observation)
        estimated_tags = self._viterbi_searching(seq_id)
        return estimated_tags

    def random_token(self):
        np.random.seed(50)
        return np.random.choice(range(self.num_tok), p=self.tok_dis_arr)

    def encode(self, observation):
        """Encode list of tokens into IDs.

        Args:
          observation: list of tokens, tokenized sentence.
        Returns:
          padded_seq_id: list of token id (int.).
        """
        if self.use_bigram:
            seq_id = list()
            # collect token in vocabulary and generated token
            generated_tokens = list()
            for idx in range(len(observation)):
                cur_tok = observation[idx]

                # ***Dealing unknown token***
                if cur_tok not in self.tok2idx:
                    if idx == 0 and self.sample_first_tok:
                        random_sent = self.rdn.choice(self.sents)
                        first_tok = random_sent[0][0]
                        tok_id = self.tok2idx[first_tok]
                        generated_tokens.append(first_tok)

                    elif idx == 0 and self.use_bigram:
                        # first_tok = ['Der']
                        first_tok = '[SOS]'
                        context_tuple = tuple([first_tok])
                        pred_tok = self.bigram[(context_tuple)].generate()
                        tok_id = self.tok2idx[pred_tok]
                        generated_tokens.append(pred_tok)
                        
                    elif idx != 0 and self.use_bigram:
                        previous_tok = observation[idx-1]
                        # use last generated token
                        if previous_tok not in self.tokens:
                            previous_tok = generated_tokens[-1]
                        context_tuple = tuple([previous_tok])
                        pred_tok = self.bigram[(context_tuple)].generate()
                        tok_id = self.tok2idx[pred_tok]
                        generated_tokens.append(pred_tok)
                else:
                    tok_id = self.tok2idx[cur_tok]
                    generated_tokens.append(cur_tok)

                seq_id.append(tok_id)
        elif self.sample_from_distribution:
            seq_id = [ self.tok2idx[tok] if tok in self.tok2idx else self.random_token() for tok in observation]
        else:
            seq_id = [ self.tok2idx[tok] if tok in self.tok2idx else self.tok2idx['Kosten'] for tok in observation]

        padded_seq_id = [0] + seq_id
        return padded_seq_id

    def _evaluate(self, eval_path, output_file):
        """Evalute HMM tagger on file.

        The function runs on Conll format file without Tag. 
        
        Args:
          eval_path: path to Conll format file.
        """
        path = os.path.join(self.data_dir, eval_path)
        with open(path, 'r', encoding='utf-8') as f:
            token_lst = f.readlines()

        sent_lst = list()
        sent_temp = list()
        for  line in token_lst:
            line = line.strip()
            if line == '' and len(sent_temp) != 0:
                sent_lst.append(sent_temp)
                sent_temp = list()
            else:
                sent_temp.append(line)

        with open(output_file, 'w', encoding='utf-8') as f:
            for sent in sent_lst:
                tags =  self.tag(sent)
                for tok, tag in zip(sent, tags):
                    f.write('{}\t{}\n'.format(tok, tag))
                f.write('\n')

    def _viterbi_searching(self, observation):
        """Implement Viterbi algorithm.
    
        Args:
          observation: sequence of observation with shape 
          init_dist: initial probability
          transition_probability: a matrix with shape (num_tag, num_tag)
          emission_probability: a matrix with shape (num_tag, num_token)
        Return:
          tag_seq: list, sequence of tags
        """
        num_tag = self.transition_probs.shape[0]
        seq_len = len(observation)

        # Initialize accumulated prob matrix
        accu_prob = np.zeros((num_tag, seq_len))
        backpointer = np.zeros((num_tag, seq_len-1)).astype(np.int32)

        # tag in first position 
        # (num_tags,) * (num_tag, 1)
        accu_prob[:, 0] = np.multiply(self.init_probs, self.emission_probs[:, 0])

        # update each entry of accumulated probability matrix
        for seq_idx in range(1, seq_len):
            for tag_idx in range(num_tag):
                # prob of current tag i from previous tags
                temp_product = np.multiply(self.transition_probs[:, tag_idx], accu_prob[:, seq_idx-1])
                accu_prob[tag_idx, seq_idx] = np.max(temp_product) * self.emission_probs[tag_idx, observation[seq_idx]]
                backpointer[tag_idx, seq_idx-1] = np.argmax(temp_product)

        # backtracking
        opt_seq = np.zeros(seq_len).astype(np.int32)
        opt_seq[-1] = np.argmax(accu_prob[:, -1])
        for n in range(seq_len-2, 0, -1):
            opt_seq[n] = backpointer[int(opt_seq[n+1]), n]

        # convert idx of tags to tag
        tag_seq = [ self.idx2tag[idx] for idx in opt_seq[1:] ]
        return tag_seq


def main():
    DATADIR = 'de-utb'
    train_file = 'de-train.tt'
    eval_file = 'de-eval.tt'
    test_file = 'de-test.t'

    # ***EXTRA CREDIT***
    hmm_tagger = HiddenMarkovTagger(data_dir=DATADIR,
                                    train_file=train_file,
                                    eval_file=test_file,
                                    use_bigram=False,
                                    sample_from_distribution=False, 
                                    sample_first_tok=False)
    # Calculate the parameters
    start = time.time()
    hmm_tagger.train(do_eval=True, output_file='o.txt')
    executed_time = round(time.time() - start, 4)
    print('Executed {} secs.'.format(executed_time))

if __name__ == '__main__':
    main()


