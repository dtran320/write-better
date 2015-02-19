from flask import Flask, Markup, render_template, request
import lxml
from lxml.html.clean import Cleaner

from app import analyze_words, analyze_sentences, analyze_text

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    if not text:
        url = request.form['url']
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        text = Markup(lxml.html.tostring(
            cleaner.clean_html(lxml.html.parse(url)))).striptags()

    result = analyze_words(text)
    sent_results = analyze_sentences(text)
    sent_variance = analyze_text(text)
    return render_template('result.html',
        results=result,
        sentence_results=sent_results,
        sent_variance=sent_variance,
    )


if __name__ == "__main__":
    app.run()
