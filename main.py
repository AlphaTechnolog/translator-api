import poe
import os
import sys

from flask import Flask, request
from dotenv import load_dotenv

poe.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

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

    where lang is the name of the language that you can translate, and don't say nothing just the format, remove any presentation text like here are the langs i can translate to as you requested, also don't present it as a list with bullets or things, just the lang."""
    
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
    
    message = f"""
        You will be a good translator which just gives the translated text, you'll receive two parameters in the next format "<original-lang>;<new-lang>;<text>", so you'll take <original-lang> as the original lang and <new-lang> as the translated lang, and <text> as the text to tranlslate, so as a translator, what you will do is just translate <text> from <original-lang> to <new-lang> (example of input "english;spanish;Hello World", you will output "Hola Mundo"), also remember the next rule, if the <text> uses some accronym like "lol" just put it's meaning, like per example, lol is "jaja" (in spanish), so if the input is "english;spanish;hello lol" you'll gimme "Hola jaja". So ended the rules, the prompt you have to translate is "{language};{dest_language};{base_text}"
    """.strip()

    for chunk in client.send_message("nutria", message):
        pass

    return {
        "language": language,
        "dest_language": dest_language,
        "base_text": base_text,
        "translatedText": chunk["text"].strip()
    }


def show_usage():
    print(f"Usage {sys.argv[0]} [--reload|-r] [--help|-h|help]")
    exit(0)


def main():
    argv = sys.argv[1:]

    with_reloading = False

    for arg in argv:
        if arg.startswith("-") and arg in ['--help', '-h', 'help']:
            return show_usage()
        elif arg.startswith("-") and arg in ['--reload', '-r']:
            with_reloading = True

    app.run(debug=with_reloading)

if __name__ == '__main__':
    main()
