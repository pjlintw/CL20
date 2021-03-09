

from collections import defaultdict




def create_translation_probs():
    """Create transaltion matrix stored by dict.


    Example:
        Ich I   -0.7091134590604324
        ich I   -0.8420319187819165
    """
    translation_prob = defaultdict(dict)

    translation_prob["DE"]["EN"] = 0.3

    print(translation_prob)
    print(translation_prob["DE"])
    return translation_prob




def stack_decoding(sentences, translation_probs):
    """Find translation by stack decoding.

    Args:
      sentences: list of sentence in string.
      translation_probs: `defaultdict(dict)` maps phrase-to-phrase-score 
    """
    translation_lst = list()

    for sentence in sentences:
        scores = defaultdict(int)
        translation_sen_lst = defaultdict(list)
        word_lst = sentence.strip().split()
        # Remove punctuation
    cnt = 1

    for i in range(len(word_lst)):
        buffer_str = ""
        for j in range(len(word_lst)-cnt+1):
            phrase = words[j:j+count]
            phrase = " ".join(phrase)
            if phrase in translation_probs:
                phrase_candidate = max(tp[phrase].items(), key=operator.itemgetter(1))[0]
                translationScore[count]+=tp[phrase][translationPhrase]
                buffer_str+=translationPhrase+' '
        if buffer_str != "":
            translation_sen_lst[count].append(buffer_str)
        cnt+=1

    index = max(translationScore.items(), key=operator.itemgetter(1))[0]
    finalTranslation = ' '.join(translation_sen_lst[index])
    print("final translation", finalTranslation)
    translation_lst.append(finalTranslation)

def main():
    stack_decoding()


if __name__ == "__main__":
    main()