import random
from flask import Flask, jsonify, request
from flasgger import Swagger
import urllib.request
from googleTranslate import translate

app = Flask(__name__)
Swagger(app)

@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
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
            text:
              type: string
              description: The text
            translation:
              type: string
              description: The translation
    """

    translation = translate(text, "sv")

    return jsonify(
        text=text,
        translation=translation
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
            text:
              type: string
              description: The text
            isGood:
              type: boolean
              description: Whether it's good or bad
    """

    isGood = text == 'yeah'

    return jsonify(
        text=text,
        isGood=isGood
    )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
