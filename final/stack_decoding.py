"""Find best sentence by stack decoding algorithm. """

import optparse
import sys
import models
import time

from collections import defaultdict, namedtuple

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/test.sentences", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation_model", dest="tm", default="data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language_model", dest="lm", default="data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxsize, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations_per_phrase", dest="k", default=1, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack_size", dest="s", default=1, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-w", "--write_file", dest="w", default="result/translation", type="str", help="File for saving translation.")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")
optparser.add_option("--iter", dest="it", default=10, type="int", help="Maximum iterations for greedy search (default=10)")
opts = optparser.parse_args()[0]

tm = models.TM(opts.tm, opts.k)
lm = models.LM(opts.lm)
french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())): # for word in vocab of input
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]


def stack_decode(f):
    """Stack decoder.
    Args:
      f: List of words in French.

    Return:
      namedtuple for translation.
    """

    hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, fr_phrase, done")
    # Check if translated
    done = [0 for i in range(len(f))]
    # Initial hypothesis & stacks 
    initial_hypothesis = hypothesis(0.0, lm.begin(), None, None, None, done) 
    stacks = [{} for _ in f] + [{}]
    stacks[0][lm.begin()] = initial_hypothesis # differentiate between stacks based on size
    for i, stack in enumerate(stacks[:-1]):  # get all but the last stack
      for h in sorted(stack.values(),key=lambda h: -h.logprob)[:opts.s]: # prune with stack size
          # get all translation options possible, and try them on h
          # Look for phrases starting anywhere, not just after i
          
          for k in range(0,len(f)): #  start of french
              for j in range(k+1,len(f)+1): # end of french
                  # check if it has already been translated in hypo
                  if any(h.done[x] for x in range(k,j)):
                      continue

                  if f[k:j] in tm: #for french phrases starting from k
                    for phrase in tm[f[k:j]]: # for all translation options
                      # copy the last done matrix - my variables names, wow
                      new_done = h.done.copy()
                      logprob = h.logprob + phrase.logprob
                      lm_state = h.lm_state

                      for word in phrase.english.split():
                        (lm_state, word_logprob) = lm.score(lm_state, word)
                        logprob += word_logprob
                      logprob += lm.end(lm_state) if j == len(f) -1 else 0.0
                      for x in range(k,j): new_done[x] = 1
                      c = new_done.count(1)

                      new_hypothesis = hypothesis(logprob, lm_state, h, phrase, f[k:j], new_done)
                      not_lm_state = ''.join(map(str,new_done)) # not saving lm_state gives better log prob
                      if not_lm_state not in stacks[c] or stacks[c][not_lm_state].logprob < logprob:
                        # recombination
                        stacks[c][not_lm_state] = new_hypothesis
    winner = max(stacks[-1].values(), key=lambda h: h.logprob)
    
    return winner


def get_phrases(hypothesis):
    """Adaptation of extract_translation() given in skeleton code.

    Args:
      hypothesis:
    """
    e_to_f = []
    f_count = 0
    while hypothesis.phrase is not None:
        e_to_f.append([hypothesis.phrase.english, hypothesis.fr_phrase])
        #print(hypothesis.phrase.english, ' ',)
        f_count+=len(hypothesis.fr_phrase)
        hypothesis = hypothesis.predecessor
    return ['na', e_to_f[::-1], f_count]


def neighbors(phrase_pairs):
    """Generate phrase by 6 operations on `move`, `swap`,
        `replace`,`bi-replace`, `split` and `merge`.
    
        English phrase: swap.
        Source, change translation: replace, bi-replace.
        French phrase: split, merge, move.
    """
    outputs = []
    # first letter in outputs is for debugging purposes only

    n = len(phrase_pairs)
    french_count = 0

    for e,f in phrase_pairs:
        french_count+=len(f)

    # Swap: swap adjacent phrases
    for i in range(n - 1):
        new_sent = phrase_pairs.copy()
        new_sent[i], new_sent[i+1] = new_sent[i+1], new_sent[i]
        outputs.append(['s', new_sent, french_count, 0.0])
        # only the alignment has changed - no difference in tm score

    # Replace: replace a translation with other translations
    for p_i in range(n):
        trs = tm[phrase_pairs[p_i][1]] # get all possible translations
        if len(trs)<2: # there can be no replacement if no other translation
            continue
        for tr in trs:
            if tr.english == phrase_pairs[p_i][0]:
                old_prob = tr.logprob # find the old probability
                break
        for tr in trs:
            # print(trs.english)
            if tr.english!=phrase_pairs[p_i][0]:
                # replace this translation
                new_sent = phrase_pairs.copy()
                new_sent[p_i][0] = tr.english
                tm_change = tr.logprob - old_prob # find probability change
                outputs.append(['r', new_sent, french_count, tm_change])


    # bi-replace: same as above, except 2 adjacent phrases get replaced
    for p_i in range(n-1):
        trs1 = tm[phrase_pairs[p_i][1]]
        trs2 = tm[phrase_pairs[p_i+1][1]]
        if len(trs1) < 2 or len(trs2) < 2:
            continue
        for tr in trs1:
            if tr.english == phrase_pairs[p_i][0]:
                old_prob = tr.logprob
                break
        for tr in trs2:
            if tr.english == phrase_pairs[p_i][0]:
                old_prob += tr.logprob
                break

        for tr1 in trs1:
            for tr2 in trs2:
                if tr1.english!=phrase_pairs[p_i][0] and tr2.english!=phrase_pairs[p_i+1][0]:
                    # replace this translation
                    new_sent = phrase_pairs.copy()
                    new_sent[p_i][0] = tr1.english
                    new_sent[p_i+1][0] = tr2.english

                    tm_change = tr1.logprob + tr2.logprob - old_prob
                    outputs.append(['b', new_sent, french_count, tm_change])


    # Split: split into 2 parts, translate
    for p_i in range(n):
        f_p = phrase_pairs[p_i][1]
        if len(f_p)>1: # if the french phrase is bigger than 1, break!
            # copy this as is
            trs = tm[f_p]
            for tr in trs:
                if tr.english == phrase_pairs[p_i][0]:
                    old_prob = tr.logprob
                    break
            for j in range(1,len(f_p)): # break point
                possible_p = phrase_pairs[:p_i]
                if (f_p[:j],) in tm and (f_p[j:],) in tm:
                    for trs1 in tm[f_p[:j]]:
                        for trs2 in tm[f_p[j:]]:
                            possible_p.append([trs1.english,f_p[:j]])
                            possible_p.append([trs2.english, f_p[j:]])
                            tm_change = trs1.logprob + trs2.logprob - old_prob
                            if p_i+1<n:
                                possible_p += phrase_pairs[p_i+1:][:]
                            outputs.append(['l',possible_p, french_count + 1, tm_change])

    # Merge - add consecutive french phrases
    for p_i in range(n-1):
        f_p1, f_p2 = phrase_pairs[p_i][1], phrase_pairs[p_i+1][1]
        merged = f_p1 + f_p2
        trs = tm[f_p1]
        for tr in trs:
            if tr.english == phrase_pairs[p_i][0]:
                old_prob = tr.logprob
                break
        trs = tm[f_p2]
        for tr in trs:
            if tr.english == phrase_pairs[p_i+1][0]:
                old_prob += tr.logprob
                break

        if merged in tm:
            for tr in tm[merged]:
                new = phrase_pairs[:p_i]
                new.append([tr.english, merged])
                tm_change = tr.logprob - old_prob
                if p_i + 2< n:
                    new += phrase_pairs[p_i + 2:]
                outputs.append(['m',new, french_count - 1, tm_change])

    return outputs


def lm_score(phrase_pairs):
    """Get language model score for translation."""
    logprob = 0.0
    lm_state = lm.begin() # </s>

    english = ''
    for e,f in phrase_pairs:
        for word in e.split():
          (lm_state, word_logprob) = lm.score(lm_state, word)
          logprob += word_logprob
    logprob += lm.end(lm_state)
    return logprob


def tm_score(pairs):
    """Get translation model score for a pair of F to E translation."""
    logprob = 0.0
    for src, tgt in pairs[1]:
        # print(eng, fr)
        if src != None:
            # translation model socre
            trs = tm[tgt]
            for tr in trs:
                if tr.english == src:
                    logprob += tr.logprob
    # print(logprob)
    return logprob


def score(outputs, tm=None, flag=False, init_prob=0):
    """Compute the score."""
    if flag:
        # if this is the hypothesis tuple
        french_count = outputs[2]
        # return init_prob - french_count
        return init_prob
    logprob = 0.0

    lm = lm_score(outputs[1])
    translated_count = outputs[2]
    tm = tm_score(outputs)

    # add tm score
    # tm += outputs[3]
    return lm + tm


def decode_greedy(seed):
    """Greedy decoder, improve the hypotheses from stack decoder.

    Paper: 'A Greedy Decoder for Phrase-Based Statistical Machine Translation'


    Args:
      seed: Namedtuple for translation. The hypothesis for the best sentence from stack decoder.
    """
    # print("seed",seed)
    current = get_phrases(seed) # will give f-e pairs
    current +=  [0.0] # tm change is 0
    init = True
    tm = tm_score(current)

    for _ in range(opts.it):  # paper used < 10, <2 in most cases
        s_cur = score(current, tm, init, init_prob = seed.logprob)
        init = False
        s = s_cur
        for hypo_stats in neighbors(current[1]):
            c = score(hypo_stats,tm)
            if c > s:
                s = c
                best = hypo_stats
        if s == s_cur:
            return current #iterate until no change in best score
        else:
            current = best
            tm = tm_score(current)


def extract_translation(pair):
    """Extract translation sentence.
    
    Args:
      pair: List of phrase pair.
             [['the Speaker :', ('le', 'Président', ':')], 
              ['Honour', ('Honneur',)], 
              ['his', ('son',)]]

    Return:
      translation: String, English translation sentence.
    """
    #print("pair", pair)
    translation = ""
    # Joint into string
    for e, f_tuple in pair:
        print(e, f_tuple)
        #french += f + " "
        translation += e + " "
    print("")
    return translation


def main():
    sys.stderr.write("Decoding %s...\n" % (opts.input,))
    start = time.time() 
        
    # Wirte file
    wf = open(opts.w, 'w')
    num_sentence = 0
    for f in french:
        # Stacking decoding
        translation = stack_decode(f)
        # print("translation pair", translation)
        # print(translation)
        final_pair = decode_greedy(translation)

        # Extract English translation
        translation_sentence = extract_translation(final_pair[1])

        # Write translation
        wf.write(f"{translation_sentence}\n")

        #sys.stderr.write("Saving translation result to ing %s...\n" % (opts.input,))
        if opts.verbose:
            tm_logprob = tm_score(final_pair)
            lm_logprob = lm_score(final_pair[1])
            sys.stderr.write("LM = %f, TM = %f, Total = %f\n" %
                (lm_logprob - tm_logprob, tm_logprob, lm_logprob))

        num_sentence +=1

    # Log time
    end=time.time()
    runtime = end-start
    avg_per_sentence = runtime / (num_sentence)
    sys.stdout.write(f"Running {runtime:.4f} seconds for {num_sentence} sentences.\n")
    sys.stdout.write(f"{avg_per_sentence:.5f} seconds per sentence.\n")


if __name__ == "__main__":
    main()



