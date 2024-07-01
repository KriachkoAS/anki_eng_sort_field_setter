from array import array
import os
import itertools
import sqlite3
from typing import NamedTuple



def get_module_dir():
    return os.path.dirname(__file__) + '\\'


def get_known_probabilities(number_of_known_words):
    """return array of known_probabilities of words with notnull ffreqs sorted by word.
known_probabilities are relevant as nearest number_of_known_words saved"""
    numbers_of_known_words_of_groups = array('i')
    with open(get_module_dir() + 'known_probability_groups', 'br') as f:
        numbers_of_known_words_of_groups.frombytes(f.read())
    number_of_known_words_index = min(range(len(array('i', [0])+numbers_of_known_words_of_groups)), key=lambda i: abs((array('i', [0])+numbers_of_known_words_of_groups)[i]-number_of_known_words-0.5))
    if number_of_known_words_index == 0:
        return itertools.cycle([0])
    number_of_known_words_index -= 1
    prob_arr = array('d')
    with open(get_module_dir() + 'known_probability_raw', 'br') as f:
        prob_arr.frombytes(f.read())
    number_of_group_words = len(prob_arr) // len(numbers_of_known_words_of_groups)
    prob_arr = prob_arr[number_of_known_words_index*number_of_group_words:(number_of_known_words_index+1)*number_of_group_words]
    return prob_arr


def get_ffreq_data_iterator(number_of_known_words):
    class FreqData(NamedTuple):
        word: str
        ffreq: float
        known_probability: float
    known_probabilities_iterator = iter(get_known_probabilities(number_of_known_words))
    with sqlite3.connect(get_module_dir() + 'ffreq.db') as conn:
        for word, ffreq in conn.execute('select * from ffreq order by word'):
            yield FreqData(word, ffreq, 0 if ffreq==0 else next(known_probabilities_iterator))