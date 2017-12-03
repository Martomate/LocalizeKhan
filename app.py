import random
from flask import Flask, jsonify, request
from flasgger import Swagger
import urllib.request
import googleTranslate
import pickle
import json
import wordlist

app = Flask(__name__)
Swagger(app)

@app.route('/', methods=['GET'])
def index():
    text = request.args.get('text', '')

    result = """
<h4>
<a href="apidocs">API documentation</a>
</h4>
<center>
<h1>
LocalizeKhan
</h1>
<textarea name="text" cols=50 rows=4 form="textForm">{value}</textarea><br /><br />
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
<table>
<tr>
  <th></th>
  <th>Translation</th>
  <th>How bad it is</th>
</tr>
<tr>
  <th>Google Translate</th>
  <td style="max-width: 350px;">{t1}</td>
  <td>{c1}</td>
</tr>
<tr>
  <th>Using wordlist</th>
  <td style="max-width: 350px;">{t2}</td>
  <td>{c2}</td>
</tr>
</table>
</div>
        """.format(t1=translationSimple, c1=classification(translationSimple), t2=translation, c2=classification(translation))

    result += "</center>"
    return result


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

    words = text.split(' ')

    for word in words:
        for phrase in wordlist.getKeysStartingWith(word):
            tr = wordlist.getTranslation(phrase)
            if (tr != None):
                translation = translation.replace(phrase, tr)

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
