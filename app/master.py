from flask import Flask, render_template, url_for, request, jsonify;
import threading;

import main;
import nlp;

app = Flask(__name__, template_folder=".\\", static_folder=".\\static");
PORT = 5001;

@app.route('/')
def start():
    return render_template("index.html");

@app.route('/reader/<chapter>', methods=["GET"])
def reader(chapter):

    t="...";

    try:

        ratio = float(request.args.get("ratio"));
        start = str(request.args.get("start")).split(".");
        distance = str(request.args.get("dist")).split(".");
    
        t = main.analize_section(
            int(start[0]) * ratio,
            int(start[1]) * ratio,
            (int(start[0]) + int(distance[0])) * ratio,
            (int(start[1]) + int(distance[1])) * ratio,
        );
    except: pass;

    return render_template("pages/reader.html", file=url_for('static', filename=chapter), text=t);

@app.route('/parser', methods=["GET"])
def parser():

    func = int(request.args.get("func"));

    if func == 0:

        # Naturally parse sentence to word list

        sentence = request.args.get("contents");
        word_list = nlp.tokenize(sentence=sentence);
        
        return jsonify({"words":[word_list]});
    elif func == 1:

        # Get word meaning and general data
        word = request.args.get("word");
        meaning: nlp.Word = nlp.find_word_meaning(word=word);
    
        if meaning == None: return jsonify({});
        return jsonify({"meaning": meaning.__dict__});
        
    elif func == 2:

        # Get example sentences
        word = request.args.get("word");
        examples = nlp.get_example_sentences(word=word);
    
        return jsonify({"examples": examples});

    else:
        return jsonify({});

if __name__ == '__main__':
    app.run('127.0.0.1', PORT);