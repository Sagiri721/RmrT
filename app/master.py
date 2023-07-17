from flask import Flask, render_template, url_for, request;
import main;

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

    return render_template("pages/reader.html", file=url_for('static', filename=main.file), text=t);

if __name__ == '__main__':
    app.run('127.0.0.1', PORT);