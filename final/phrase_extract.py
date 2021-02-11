"""Build phrase translation table"""

srctext = "michael assumes that he will stay in the house"
tgttext = "michael geht davon aus , dass er im haus bleibt"
alignment = [(0,0), (1,1), (1,2), (1,3), (2,5), (3,6), (4,9), 
            (5,9), (6,7), (7,7), (8,8)]


def phrase_extract(src_text, tgt_text, alignment):
    """"""

    for e, f in alignment:
        if (f_start <= f <= f_end) and (e < e_start or e > e_end):
            return {}

    return None

phrase_extract(srctext, tgttext, alignment)