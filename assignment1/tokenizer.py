"""Tokenize raw text."""

import nltk
import sentencepiece as spm
from logging import getLogger

logger = getLogger()

TOKENIZ = {
        'word-en': nltk.word_tokenize,
        }

class VilinaTokenizer:
    def __init__(self, config):
        self.voab = _get_vocab

    def tokenize(self):
        pass
    def detokenie(self):
        pass
    def encode(self):
        pass
    def decode(self):
        pass
    def _get_vocab(self):
        pass

class SMPTokenizer:
    def __init__(self, config):
        pass
    def tokenize(self):
        pass
    def detokenize(self):
        pass
    def encode(self):
        pass
    def decode(self):
        pass
