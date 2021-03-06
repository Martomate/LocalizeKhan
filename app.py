import random
from flask import Flask, jsonify, request
from flasgger import Swagger
import urllib.request
import google_translate
import pickle
import json
import wordlist

app = Flask(__name__)
Swagger(app)

@app.route('/', methods=['GET'])
def index():
    return index1(request.args.get('text', ''))

def index1(text):
    result = """
<h4>
<a href="apidocs">API documentation</a>
</h4>
<center>
<h1>
LocalizeKhan
</h1>
<textarea name="text" cols=50 rows=4 maxlength=1500 form="textForm">{value}</textarea><br /><br />
<form action="." id="textForm">
<input type="submit" value="Translate">
</form>
    """.format(value=text)

    if (text != ''):
        translationSimple = translateSimple(text)
        translation = translateAdvanced(text)
        result += """
<br />
<div id="result">
<table border=1 style="border-collapse: collapse" cellpadding=10>
<tr>
  <th></th>
  <th>Google</th>
  <th>Improved</th>
</tr>
<tr>
  <th>Translation</th>
  <td style="max-width: 350px;">{t1}</td>
  <td style="max-width: 350px;">{t2}</td>
</tr>
<tr>
  <th>Quality</th>
  <td>{c1}</td>
  <td>{c2}</td>
</tr>
</table>
</div>
        """.format(t1=translationSimple, c1=classification(translationSimple), t2=translation, c2=classification(translation))

    result += "</center>"
    return result


@app.route('/api/translateAll/<string:text>/', methods=['GET'])
def translateAllIndex(text):
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
            google_translation:
              type: string
              description: The translation
            google_quality:
              type: number
              description: How good it is
            improved_translation:
              type: string
              description: The improved translation
            improved_quality:
              type: number
              description: How good it is
    """

    gt = translateSimple(text)
    tt = translateAdvanced(text)
    return jsonify(
        google_translation=gt,
        google_quality=classification(gt),
        improved_translation=tt,
        improved_quality=classification(tt)
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
            quality:
              type: number
              description: How good it is
    """

    return jsonify(
        quality=classification(text)
    )

def translateSimple(text):
    return google_translate.translate(text, 'sv')

def translateAdvanced(text):
    words = text.split(' ')
    for word in words:
        for phrase in wordlist.getKeysStartingWith(word):
            tr = wordlist.getTranslation(phrase)
            if (tr != None):
                text = text.replace(phrase, tr)

    return translateSimple(text)

def classification(text):
    text = [text]

    clf_name = 'clf_dummy'
    clf = pickle.load(open(clf_name, 'rb'))
    prob = clf.predict_proba(text)
    prob = prob[0][0]

    return prob


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
