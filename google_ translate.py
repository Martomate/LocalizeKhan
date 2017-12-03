# Imports the Google Cloud client library
from google.cloud import translate


# Instantiates a client
translate_client = translate.Client()

def translate(text, target_language):
	translation = translate_client.translate(
	    text,
	    target_language)

	return translation['translatedText']





