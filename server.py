from flask import Flask, render_template, request

from app import analyze_words

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    result = analyze_words(request.form['text'])
    return render_template('result.html', results=result)



if __name__ == "__main__":
    app.run()
