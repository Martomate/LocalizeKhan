# LocalizeKhan
Our solution improves the process of proofreading by automatically classifying translated texts to determine the quality of the translation. The idea is to minimize the amount of tedious manual work of proofreading texts.

Please note: The classifier has not yet been trained with very much data.

# Setup

```bash
pip install google-cloud-translate Flask flasgger sklearn # See requirements.txt for all dependencies.
export FLASK_APP=app.py
flask run
```

To be able to use Google's service for automatic translation it's required to set up a authentication, see [https://cloud.google.com/docs/authentication/getting-started](https://cloud.google.com/docs/authentication/getting-started)
