import random
from flask import Flask, jsonify, request
from flasgger import Swagger
import urllib.request
import googleTranslate
import pickle
import json
#import wordlist

app = Flask(__name__)
Swagger(app)
"""
@app.route('/', methods=['GET'])
def index():
    text = request.args.get('text', '')
    translationSimple = translateSimple(text)
    translation = translateAdvanced(text)
    return jsonify(
        translationWithoutWordlist=translationSimple,
        classificationWithoutWordlist=classification(translationSimple),
        translation=translation,
        classification=classification(translation)
    )
"""

@app.route('/api/translate/<string:text>/', methods=['GET'])
def translateIndex(text):
    """
    This is the translator API
    Call this api passing a piece of text and get back the Swedish translation
    ---
    tags:
      - Translation API
    parameters:
      - name: text
        in: path
        type: string
        required: true
        description: The text
    responses:
      200:
        description: Whether it's good or bad
        schema:
          id: translate
          properties:
            translation:
              type: string
              description: The translation
    """

    return jsonify(
        translation=translateAdvanced(text)
    )

@app.route('/api/classifier/<string:text>/', methods=['GET'])
def classificationIndex(text):
    """
    This is the classifier API
    Call this api passing a piece of text and get back whether it's good or not
    ---
    tags:
      - Classification API
    parameters:
      - name: text
        in: path
        type: string
        required: true
        description: The text
    responses:
      200:
        description: Whether it's good or bad
        schema:
          id: classifier
          properties:
            isGood:
              type: number
              description: Whether it's good or bad
    """

    return jsonify(
        isGood=classification(text)
    )

def translateSimple(text):
    translation = googleTranslate.translate(text, 'sv')
    return translation

def translateAdvanced(text):
    translation = translateSimple(text)
    """
    words = text.split(' ')

    for word in words:
        for phrase in wordlist.getKeysStartingWith(word):
            tr = wordlist.getTranslation(phrase)
            if (tr != None) translation = translation.replace(phrase, tr)
    """
    return translation

def classification(text):
    text = [text]

    clf_name = 'clf_dummy'
    clf = pickle.load(open(clf_name, 'rb'))
    prob = clf.predict_proba(text)
    prob = prob[0][0]

    return prob


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
