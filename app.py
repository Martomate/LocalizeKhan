import random
from flask import Flask, jsonify, request
from flasgger import Swagger
import urllib.request
from googleTranslate import translate
import pickle
import json

app = Flask(__name__)
Swagger(app)

@app.route('/', methods=['GET'])
def index():
    text = request.args.get('text', '')
    translation = translate(text, 'sv')
    classif = classification(text)
    return jsonify(
        translation=translation,
        classification=classif
    )


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
        translation=translate(text, "sv")
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
    text = [text]
    print('Text is {}'.format(text))
    clf_name = 'classifier'
    clf = pickle.load(open(clf_name, 'rb'))
    prob = clf.predict_proba(text)
    print(prob)
    prob = prob[0][0]
    print('Sliced prob',prob)
    return jsonify(
        isGood=prob
    )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
