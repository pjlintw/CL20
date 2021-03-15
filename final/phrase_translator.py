"""Build phrase translation table from source, target sentences and word alignments."""

import sys
import math
import argparse
from pathlib import Path
from collections import defaultdict

import time

def read_file(file):
    with open(file, 'r') as f:
        data = [line.strip() for line in f]
    return data

def read_alignment(file):
    """Read aligment file.

    Hansard alignment is expected.
    """
    alignments = list()
    with open(file, 'r') as f:
        for line in f:
            line_lst = line.strip().split()
            align_lst = list()
            for pair in line_lst:
                src_idx, tgt_idx = pair.split('-')
                align_lst.append((int(src_idx),int(tgt_idx)))
            # print(align_lst)
            alignments.append(align_lst)
    return alignments
    

class PhraseTranslationModel:
    def __init__(self):
        pass

    ##### FEATRUE: Phrase Table Exraction #####
    def extract_phrase(self, src_text, tgt_text, alignment, max_phrase_len=0):
        """Extract all phrases from word alignment.
        
        Args:
          src_text: String, a sentence in source (foreign) language.
          tgt_text: String, a sentence in target langugage.
          alignment: List of tuple. The word-to-word alignments.
                    [(1,1), (1,2), (2,3)]
          max_phrase_len: Intege, maximal length for possible phrase. No limited if 0. 
        
        Returns:
          A set of tuples made of (1) index (2)(2)
        """
        def extract_from_range(tgt_start, tgt_end, src_start, src_end, max_phrase_len):
            """Extract a set of possible phrase given the source, language ranges.

            """
            # print("rages", tgt_start, tgt_end, src_start, src_end)
            if tgt_end < 0:
                return 
            # If `src_align_idx` out of the `src_start` and `src_target`.
            for src_align_idx, tgt_align_idx in alignment:
                 # target align point
                 # sorce align point out of range
                if ((tgt_start <= tgt_align_idx <= tgt_end) and        
                   (src_align_idx < src_start or  src_align_idx > src_end)):  
                    return
            phrase_set = set()
            ts = tgt_start # For increment
            while True:
                te = min(tgt_end, ts+max_phrase_len-1) # For decrement
                # te = tgt_end 
                while True:
                    # Add phrase pair (src_start, src_end, tgt_start, tgt_end)
                    src_phrase = " ".join(src_sent[i] for i in range(src_start,src_end+1))
                    tgt_phrase = " ".join(tgt_sent[i] for i in range(ts,te+1))
                    phrase_set.add(((src_start, src_end+1), src_phrase, tgt_phrase))
                    te+= 1
                    # Add phrase until `te` aligned or out of range
                    if te in tgt_aligned or te == tgt_len:
                        break
                ts-=1
                # Add phrase until `te` aligned or out of range
                if ts in tgt_aligned or ts < 0:
                    break
            
            return phrase_set

        # List of words
        src_sent = src_text.split()
        tgt_sent = tgt_text.split()
        
        # Set ot collect hrases
        phrase_set = set()
        
        # Length of sentences  
        src_len = len(src_sent)
        tgt_len = len(tgt_sent)

        # Target language's align points
        tgt_aligned = [tgt_idx for _,tgt_idx in alignment ]
        max_phrase_len = max_phrase_len or max(src_len, tgt_len)


        ### Extraction ##### 
        # Two steps:
        # (1) Loop all possible soruce language phrases matching minimal target language phrases
        # (2) By finding shortest target language phrases that includes 
        #     all the foreign counterparts for the source words.
        #
        ### Extraction #####
        # Go over each source substring starting from begin 
        for src_start in range(src_len):
            # Set maximal length for phrase length 
            max_idx = min(src_len, src_start+max_phrase_len)
            for src_end in range(src_start, max_idx):
                # print('src_start, end', src_start, src_end)
                # Find the minimal matching of foreign phrase
                tgt_start, tgt_end = tgt_len-1, -1
                for src_align_idx, tgt_align_idx in alignment:
                    # print('alignment', src_align_idx, tgt_align_idx)
                    # Length of phrase is greater or equal to one
                    if src_start <= src_align_idx <= src_end:
                        # print(tgt_align_idx, tgt_start, tgt_end)
                        # Longest substring in target langage phrase
                        tgt_start = min(tgt_align_idx, tgt_start)
                        tgt_end = max(tgt_align_idx, tgt_end)
                        # print(tgt_start, tgt_end, end='\n\n')
                # print(src_start, src_end)
                # print(tgt_start, tgt_end, end='\n\n')
                # Extract a set of phrases 
                phrase = extract_from_range(tgt_start, tgt_end, src_start, src_end,max_phrase_len)
                if phrase:
                    phrase_set.update(phrase)


        return phrase_set

    def extract_phrase_from_parallel_sentences(self, src_lst, 
                                               tgt_lst,
                                               word_alignment,
                                               max_phrase_len=0,
                                               save_phrase_table=None):
        """Extract phrase from list of the parallel sentences.

        Args:
          src_lst: List of sentence in string
          tgt_lst: List of sentence in string
          alignments:  List of list contains alignments
                      [[(1,1), (2,2)],  # first parallel sentence
                       [(1,2), (2,2)]   # second parallel sentence
                      ]
        
          max_phrase_len: integer, maximal length of phrase.
          save_phrase_table: string. Save the phrase file if a file given

        Returns:
            phrase_collector: 2-D lists. Each contains a list of phrses.
            flatten_phrase_lst: A list contains all phrase pairs.
        """
        # asser equal length
        assert len(src_lst) == len(tgt_lst) == len(word_alignment)
        
        # Collect all phrase        
        # Convert to list of source and target phrase pair 
        #  [("Wiederaufnahme der Sitzungsperiode", "Resumption of the session"),
        #   ("Ich bitte", "Please rise then"), 
        #   ("Das Parlament",    "The House rose and")] 
        flatten_phrase_lst = list()

        # Extract all phrases for word alignment by `extract_phrase()`
        phrase_collector = list()
        total_num = 0

        start = time.time() 
        for idx, triplet in enumerate(zip(src_lst, tgt_lst, word_alignment)):
            if (idx+1) % 5000 == 0:
                sys.stdout.write(f"Extracting phrases for {idx+1} sentences...\n")

            src_text, tgt_text, alignment = triplet 
            phrase_set = self.extract_phrase(src_text, tgt_text, alignment, max_phrase_len)
            #print("extracted phrase", phrase_set)
            phrase_collector.append(phrase_set)

            #print("number of phrase", len(phrase_set), end="\n")
            total_num+= len(phrase_set)

            # Get source phrase and target phrase into a list
            flatten_phrase_lst.extend([ (tup[1], tup[2]) for tup in phrase_set])
        end=time.time()
        runtime = end-start
        avg_per_sentence = runtime / (idx+1)
        sys.stdout.write(f"Running {runtime:.4f} seconds for {idx+1} sentences.\n")
        sys.stdout.write(f"{avg_per_sentence:.5f} seconds per sentence.\n")
            
        # # Sort according the source phrase's length 
        for idx, phrase_set in enumerate(phrase_collector):
            # Collect all English phrases for the corresponding phrase in German language.
            # {"English phrase": [(English alignment), [(German phrase),(German phrase)]], ..., ...}
            # {"assumes": [(0,1), ["geht davon aus", "geht davon aus, "]]}
            dlist = {}
            for alignment, src_phrase, tgt_phrase in phrase_set:
                
                if src_phrase in dlist:
                    dlist[src_phrase][1].append(tgt_phrase)
                else:
                    dlist[src_phrase] = [alignment, [tgt_phrase]]

            # Sort the list of translations based on their length.  Shorter phrases first.
            for v in dlist.values():
                v[1].sort(key=lambda x: len(x))

            # List of phrase contans a tuple of `source phrase`, [(source alignment), [phrase,phrase]]
            sorted_phrase_list = sorted(dlist.items(), key=lambda x:x[1])
            # update it
            phrase_collector[idx] = sorted_phrase_list


        # Save phrase file
        if save_phrase_table is not None:
            with Path(save_phrase_table).open("w") as wf:
                for phrase_lst in phrase_collector:
                    for i, p in enumerate(phrase_lst):
                        k, v = p
                        joint_phrase = "; ".join(v[1])
                        wf.write(f"{i} | {v[0]} | {k} | {joint_phrase}\n")
                        #print("({0:2}) {1} {2} — {3}".format( i, v[0], k, " ; ".join(v[1])))
            sys.stdout.write(f"Saving phrase file to path: {save_phrase_table}.\n")
        
        return phrase_collector, flatten_phrase_lst,total_num


    def compute_log_probs(self, phrases, save_to_file=None):
        """Compute log probability of soruce-target phrase pairs.

        Note that we compute log p(f|e) due to the noise channel assumption.
        Which is:
                count(French, English) / count(English) 

        Args:
          phrases: List of tuple contains source phrases and target phrases.

        Examples:
            [ (Source phrase, Target phrase), ...]
            [("Das Parlament", "The House"), ("Ich bin", "I am")]
        """
        # Co-ocurrence for source and target phrase
        tgt_src_cnt = defaultdict(lambda: defaultdict(int))
        
        # ocurrence for target (English)
        tgt_cnt = defaultdict(int)

        # Compute frequency and co-occurence
        for phrase_pair in phrases:

            assert len(phrase_pair) == 2
            src_p, tgt_p = phrase_pair
            # defaultdict[target_phrase][source_phrase]
            tgt_src_cnt[tgt_p][src_p]+=1
            # defaultdict[target_phrase]
            tgt_cnt[tgt_p]+=1


        # Calculate log prob of translation model p(f|e)
        log_prob_lst = list()
        for tgt_phrase in tgt_src_cnt:
            for src_phrase in tgt_src_cnt[tgt_phrase]:
                # count(source, target) / count(target)
                prob = float(tgt_src_cnt[tgt_phrase][src_phrase])/tgt_cnt[tgt_phrase]
                log_prob = math.log(prob)

                log_prob_str = f"{src_phrase} ||| {tgt_phrase} ||| {str(log_prob)}"
                log_prob_lst.append(log_prob_str)
        
        # Save to file 
        if save_to_file is not None:
            with Path(save_to_file).open("w") as wf:
                wf.write('\n'.join(log_prob_lst))
            sys.stdout.write(f"Saving phrase log probability file to path: {save_to_file}.\n")
    
        # List of log probability for phrase pair
        return log_prob_lst 



def flatten_phrase_collect(phrase_collect):
    """Flatten nested list into a list of soruce-target phrase pairs.

    Args:
      phrase_collect: Nested list. The inner list contains tuple of
                     (source phrase, [(aligmnet), ["target phrase", "target phrase"]]) 
                     as elements.
    Returns: A list of phrase pairs.
    """
    flatten_phrse_collect = list()
    for phrase_lst in phrase_collect:
        pass

    return flatten_phrse_collect

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_file', type=str, action='store', default=None,
                        help='source sentence file.')

    parser.add_argument('--target_file', type=str, action='store', default=None, 
                        help='target sentence file.')

    parser.add_argument('--align_file', type=str, action='store', default=None,
                        help="word-to-word alignments.")

    parser.add_argument("--output_file", type=str, action='store', default=None,
                        help="File to save log probability of the extracted phrases.")

    parser.add_argument("--save_phrase_table", type=str, action='store', default=None,
                        help="Whether save the phrase file.")

    parser.add_argument("--max_phrase_len", type=int, action='store', default=4,
                        help="Maximal length for phrase.")

    args = parser.parse_args()

    # Log out max_phrase_len
    sys.stdout.write(f"Maximal phrase length {args.max_phrase_len}.\n")

    # Ceate model
    translator = PhraseTranslationModel()

    # List of sentence in string
    src_lst = read_file(args.source_file)
    tgt_lst = read_file(args.target_file)
    # print(src_lst)

    # List of list contains alignments
    # Example:
    #   [[(1,1), (2,2)],  # first parallel sentence
    #    [(1,2), (2,2)]   # second parallel sentence
    #   ]
    alignments = read_alignment(args.align_file)

    assert len(src_lst) == len(tgt_lst) == len(alignments)

    ### Note ###
    # The methods returns two tpyes of phrase list.
    # (1)`phrase_collect`: nested list. The inner list contains tuple of
    #                      (source phrase, [(aligmnet), ["target phrase", "target phrase"]]) 
    #                       as elements
    # (2) `flatten_phrase_lst`: 1-D list for all phrase pairs:  
    #                           [(src_phrase, tgt_phrase),
    #                            (src_phrase, tgt_phrase), ...]
    phrase_collect, flatten_phrase_lst,total_num = translator.extract_phrase_from_parallel_sentences(src_lst=src_lst, 
                                                                    tgt_lst=tgt_lst,
                                                                    word_alignment=alignments,
                                                                    save_phrase_table=args.save_phrase_table,
                                                                    max_phrase_len=args.max_phrase_len)    
    
    sys.stdout.write(f"Extract {total_num} phrases.\n")

    # Log probability of phrases: log p(f|e)
    log_probs = translator.compute_log_probs(phrases=flatten_phrase_lst, save_to_file=args.output_file)
    

if __name__ == "__main__":
    main()






