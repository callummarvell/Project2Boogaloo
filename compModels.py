# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 12:23:36 2019

@author: callu
"""
from gensim.models import Word2Vec, KeyedVectors
import numpy as np
old = KeyedVectors.load_word2vec_format("modelMega3.bin", binary=True)
old.init_sims(replace=True)
model = KeyedVectors.load_word2vec_format("modelMega4.bin", binary=True)
model.init_sims(replace=True)
model5 = KeyedVectors.load_word2vec_format("modelMega4.bin", binary=True)
model5.init_sims(replace=True)

#print(old.most_similar("hot", topn=5))
print(model.most_similar("hot", topn=5))
#print(old.wv.vocab[:500])
print(dict(list(model.wv.vocab.items())[0:200]))
print(len(old.wv.vocab))
print(len(model.wv.vocab))
print(len(model5.wv.vocab))

print(old.most_similar("hot", topn=5))
print(model.most_similar("hot", topn=5))
print(model5.most_similar("hot", topn=5))