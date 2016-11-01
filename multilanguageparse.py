import numpy
import pandas as pd

import pattern

from pattern.en import parsetree as en_parse
from pattern.fr import parsetree as fr_parse
from pattern.de import parsetree as de_parse
from pattern.es import parsetree as es_parse
import langdetect

import multiprocessing

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def nounify(in_text):
    noun_text = ''
    bad_text = False
    in_text = in_text.decode('latin1')
    try:
        langdetect.detect(in_text)
    except:
        return noun_text
    if(langdetect.detect(in_text)=='en'):
        parsed_text = en_parse(in_text,lemmata=True,tokenize=True,encoding = 'utf-8')
    if(langdetect.detect(in_text)=='es'):
        parsed_text = es_parse(in_text,lemmata=True,tokenize=True,encoding = 'utf-8')
    elif(langdetect.detect(in_text)=='de'):
        parsed_text = de_parse(in_text,lemmata=True,tokenize=True,encoding = 'utf-8')
    elif(langdetect.detect(in_text)=='fr'):
        parsed_text = fr_parse(in_text,lemmata=True,tokenize=True,encoding = 'utf-8')
    else:
        bad_text = True
    if(not(bad_text)):
        for s in parsed_text.sentences:
            for c in s.chunks:
                for word in c.words:
                    if('NN' in word.part_of_speech):
                        noun_text+=word.string+' '  
    return noun_text


def noun_apply(df):
    res = df.apply(nounify)
    return res

if __name__ == '__main__':
  pool = multiprocessing.Pool(8)

  in_labelling = pd.read_csv('data/input-data-labeling.csv',encoding='utf-8')
  name_results = pool.map(noun_apply, numpy.array_split(in_labelling['name'],8))
  pool.close()
  pool.join()
  in_labelling['name'] = pd.concat(name_results, axis=0)

  pool = multiprocessing.Pool(8)

  desc_results = pool.map(noun_apply, numpy.array_split(in_labelling['description'],8))
  pool.close()
  pool.join()
  in_labelling['description'] = pd.concat(desc_results, axis=0)

  in_labelling.to_csv('parsed_fashion.csv', encoding='utf-8')

