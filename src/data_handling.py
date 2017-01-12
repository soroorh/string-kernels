import os
import string
import cPickle as pickle

import nltk

from nltk.corpus import stopwords
from bs4 import BeautifulSoup


def load_sgml_data(data_dir):
    """
    Load and parse training and test data from the Reuters dataset in SGML format
    Use Modified Apte dataset split
    :return: List with training data and list with test data
    """

    train_data = []
    test_data = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.sgm'):
            file_content = BeautifulSoup(open(os.path.join(data_dir, file_name)), 'lxml')
            train_tags = file_content.find_all('reuters', lewissplit='TRAIN', topics='YES')
            train_data += [parse_document(tag) for tag in train_tags]

            test_tags = file_content.find_all('reuters', lewissplit='TEST', topics='YES')
            test_data += [parse_document(tag) for tag in test_tags]

    return train_data, test_data


def load_cleaned_data(train_data_path, test_data_path):
    with open(train_data_path) as fd:
        train_data = pickle.load(fd)

    with open(test_data_path) as fd:
        test_data = pickle.load(fd)

    return train_data, test_data


def parse_document(tag):
    """
    Retrieve article body and topic list from tag structure.
    :param tag: Tag structure with article data
    :return: Tuple holding the document body and topic list
    """

    topics = [unicode(d_tag.text) for d_tag in tag.find('topics').find_all('d')]
    text_tag = tag.find('text')
    text = text_tag.body.text if text_tag.body else text_tag.contents[-1]

    return unicode(text), topics


def clean_document(text, blacklist):
    """
    Tokenize and filter out words present on blacklist. Change tokens to lowercase.
    :param text: document to be cleaned
    :param blacklist: word blacklist
    :return: clean document as one string with tokens separate by whitespace

    blacklist = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
    """
    tokens = nltk.word_tokenize(text)
    filtered = [token.lower() for token in tokens if token.lower() not in blacklist]
    return ' '.join(filtered)


