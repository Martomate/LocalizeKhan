#!/usr/bin/env python3
import numpy as np
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from nltk.tokenize import sent_tokenize

from googletrans import Translator


def load_hamspam(nbr_data=5172):
    # Load dummy data (mail spam)
    all_ham = os.listdir('ham/') #3672
    all_spam = os.listdir('spam/') # 1500

    in_data = []
    N = int(nbr_data / 2)
    for fname in all_ham[:N]:
        with open('ham/{}'.format(fname)) as f:
            try:
                text = f.readlines()
                text = [t.strip('\n') for t in text]
                text = "".join(text)
                in_data.append(text)
            except:
                #TODO: Handle exceptions
                pass

    nbr_ham = len(in_data)

    for fname in all_spam[:N]:
        with open('spam/{}'.format(fname)) as f:
            try:
                text = f.readlines()
                text = [t.strip('\n') for t in text]
                text = "".join(text)
                in_data.append(text)
            except:
                #TODO: Handle exceptions
                pass

    nbr_spam = len(in_data) - nbr_ham
    out_data = np.concatenate([np.zeros(nbr_ham, dtype=int), np.ones(nbr_spam, dtype=int)], axis=0)
    return in_data, out_data


def translate_text(text, src='en', dest='sv'):
    translator = Translator()
    swe_text = translator.translate(text, dest=dest, src=src)
    return swe_text.text


def save_good_data(fin, fout):
    with open(fin, 'r') as f:
        file_text = f.readline().strip('\n')
        file_text = sent_tokenize(file_text)

    with open(fout, 'w') as f:
        cls = 1
        for text in file_text:
            f.write("'{}', {} \n".format(text, cls))


def load_training_data(fname):
    X = []
    y = []
    with open(fname, 'r') as f:
        line = f.readline().strip('\n')
        while line:
            Xt, yt = line.split("',")
            X.append(Xt[1:])
            y.append(int(yt))

            line = f.readline().strip('\n')
    return X, y


def classify_text(fin, fout):
    with open(fin, 'r') as f:
        file_text = f.readline().strip('\n')
        file_text = sent_tokenize(file_text)
    print('Loading data')
    swe_text = [translate_text(text) for text in file_text]

    print('Start labeling!')
    with open(fout, 'a') as f:
        for (pre_text, post_text) in zip(file_text, swe_text):
            print('\n####Press 22 to quit####\n')
            print('Original text: \n\n {}'.format(pre_text))
            print('\nTranslated text: \n\n {}'.format(post_text))

            cls = -1
            while cls < 0 or cls > 1:
                try:
                    cls = int(input('Is this text bad? 1 = yes, 0 = no\n'))
                    if cls == 22:
                        break
                except ValueError:
                    pass

            if cls == 22:
                break
            f.write("'{}', {} \n".format(post_text, cls))


def merge_data(loc = 'training_data', fout='training_data.txt'):
    fnames = os.listdir(loc)

    in_data = []
    out_data = []

    for fname in fnames:
        with open('{}/{}'.format(loc,fname)) as f:
            line = f.readline()

            while line:
                line = line.strip('\n ')[1:].split("', ")
                in_data.append(line[0])
                try:
                    out_data.append(line[1])
                except:
                    pass #Parse error
                line = f.readline()

    with open(fout, 'w') as f:
        for (X, y) in zip(in_data, out_data):
            f.write("'{}', {} \n".format(X, y))


def train_new_classifier(data_fname, clf_name=None, spam=False, verbose=False, clf_out=False):
    # clf_name = to save classifier file name
    # data_fname = training data file name
    # NB: only 80% of data is used. 20% is used for model validation,
    # i.e not all data is used for model building
    #TODO:  - Train model with all data
    #       - Parameter tuning
    #       - Data representation: natural language processing
    if spam:
        in_data, out_data = load_hamspam()
    else:
        in_data, out_data = load_training_data(data_fname)

    X_train, X_test, y_train, y_test = train_test_split(in_data, out_data)
    pipeline = make_pipeline(CountVectorizer(), TfidfTransformer(), MultinomialNB())

    param_grid = {}
    grid_pipeline = GridSearchCV(pipeline, param_grid=param_grid, cv=4, n_jobs=1)
    grid_pipeline.fit(X_train, y_train)

    # Short test
    score_test = grid_pipeline.score(X_train, y_train)
    score_train = grid_pipeline.score(X_test, y_test)

    if verbose:
        print('Training data score: {}'.format(score_test))
        print('Test data score: {}'.format(score_train))

    # Save classifier
    if clf_name:
        pickle.dump(grid_pipeline, open(clf_name, 'wb'))

    if clf_out:
        return score_train, score_test, grid_pipeline
    else:
        return score_train, score_test


def average_performance(fname):
    N = 100
    mtrain = []
    mtest = []
    for i in range(N):
        score_train, score_test = train_new_classifier(fname)
        mtrain.append(score_train)
        mtest.append(score_test)

    mtrain = np.array(mtrain)
    mtest = np.array(mtest)

    print('Average train performance: ', mtest.mean())
    print('Average test performance: ', mtrain.mean())

    return mtrain, mtest


if __name__ == '__main__':
    # TRAIN NEW CLASSIFIER HERE
    training_data = 'training_data.txt'
    clf_name = 'classifier'
    train_new_classifier(training_data, clf_name=clf_name)

    #mtrain, mtest = average_performance(training_data)
