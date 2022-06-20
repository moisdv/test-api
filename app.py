from flask import Flask, render_template, jsonify, request, redirect, url_for

import processor



app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())


@app.route('/', methods=["GET", "POST"])
def conoceme():
    return render_template('conoceme.html', **locals())

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        the_question = request.form['question']
        if len(the_question) <= 0:
            return  jsonify({"response": "La pregunta esta en blanco" })
        response = processor.chatbot_response(the_question)

    return jsonify({"response": response })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
