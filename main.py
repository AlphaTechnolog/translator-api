import poe
import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()


def get_client() -> str:
    token = os.getenv("POE_TOKEN")
    if not token:
        raise RuntimeError("Please provide a poe token in the POE_TOKEN environment variable")

    try:
        print("Connecting to poe...")
        client = poe.Client(token)
    except Exception as excp:
        print("Failed to connect to poe due to " + str(excp))
        exit(1)

    print("Connected to poe successfully")

    return client


app = Flask(__name__)
client = get_client()


@app.route("/get-languages")
def get_languages():
    message = """gimme a little list with the languages that you are able to translate to, gimme them in the next format

    <lang>\\n

    where lang is the name of the language that you can translate"""
    
    for chunk in client.send_message("nutria", message):
        pass

    languages_str = chunk['text'].strip()
    languages = []
    for language in languages_str.split("\n"):
        languages.append(language.strip())

    return {
        "languages": languages
    }


@app.route('/translate')
def translate():
    language = request.args.get("language")
    dest_language = request.args.get("dest_language")
    base_text = request.args.get("base_text")
    if not language or not dest_language or not base_text:
        return {"error": "invalid arguments provided, check again and try later"}

    message = f"Translate '{base_text}' from {language} to {dest_language}, remember to just give the text not any other thing like `'text' translates to 'translatedText' in 'originalLang'`, where text can be my text, translatedText is the translatedText and originalLang is per example English, just return the translatedText and without quotes at first, just `translatedText`, remember to don't put a little dot if the text doesn't haves it, also if you made an error doing the translation, and you realize it, don't apologize, just remember the format and skip errors, they doesn't matters but still try to make the translations as accuracy as possible. if the phrase uses something lmao, or accronyms in any language, just put something like `'text'` where text now is one of your known meanings for that accronym, example `lmao` from english to spanish just return `me estoy riendo muchísimo`, also don't put the resultant translation with double quotes or single quotes."
    for chunk in client.send_message("nutria", message):
        pass

    return {
        "language": language,
        "dest_language": dest_language,
        "base_text": base_text,
        "translatedText": chunk["text"].strip()
    }


if __name__ == '__main__':
    app.run()
