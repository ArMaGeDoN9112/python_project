"""

This module is the entrypoint of application.


"""


import json
import os
import time
import subprocess

from typing import Dict
from hashlib import sha256

from flask import Flask, request, jsonify, render_template, Response, send_file
from flask_sock import Sock

import fer

app = Flask(__name__)
sock = Sock(app)


@app.route("/<lng>")
def index(lng):
    # template_lang = request.args.get("template_color") == 'black'
    return render_template("index.html", lang=lng)


@app.route("/")
def index_ru():
    # template_lang = request.args.get("template_color") == 'black'
    return render_template("index.html", lang="ru")


# @app.route('/en')
# def lang_en():
#     return render_template('index.html', lang='en')
#
# @app.route('/ru')
# def lang_ru():
#     return render_template('index.html', lang='ru')
#
# @app.route('/zh')
# def lang_zh():
#     return render_template('index.html', lang='zh')


@app.route("/api/upload-file", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    ext = file.filename.split(".")[1]

    key = sha256(time.time().hex().encode()).hexdigest()
    file.save(f"audio/_{key}.{ext}")
    with subprocess.Popen(
        f"ffmpeg -i audio/_{key}.{ext} "
        f"-ar 16000 "
        f"-ac 1 "
        f"-acodec pcm_s16le "
        f"audio/{key}.wav".split(),
        stdout=subprocess.PIPE,
    ) as _:
        pass

    os.remove(f"audio/_{key}.{ext}")
    return jsonify({"key": key}), 200


def gen(camera):
    while True:
        frame = camera.get_video()
        yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + \
            frame + b"\r\n\r\n"


@app.route("/api/video-feed/<key>")
def video_feed(key):
    file_name = f"audio/{key}.mp4"
    return Response(
        gen(fer.VideoCamera(file_name)),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/api/get-statistic/<key>")
def get_stat(key):
    filename = f"./statistic/{key}.png"
    response = send_file(filename, mimetype='image/png')
    os.remove(filename)

    return response

@app.route("/api/download-file/<key>")
def download_file(key):
    filename = f"./files/{key}.docx"
    response = send_file(filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    os.remove(filename)

    return response

@sock.route("/api/analyze")
def start_analyze(_sock):
    key = _sock.receive()
    use_colors = _sock.receive()
    gen_statistic = _sock.receive()

    if not os.path.isfile(f"audio/{key}.wav"):
        _sock.send(json.dumps({"result": "WRONG"}))
        return

    _sock.send(json.dumps({"result": "OK"}))
    proc = subprocess.Popen(
        ["python3", "analyze.py", f"{key}.wav", f"{use_colors}", f"{gen_statistic}"], stdout=subprocess.PIPE
    )

    while True:
        # for i in range(1000):
        #     sock.send(json.dumps({"result": "OK", "string": "ASaD@1"}, ensure_ascii=False))
        s = proc.stdout.readline().decode().replace("\n", "")

        if not s and proc.poll() is not None:
            proc.terminate()
            os.remove(f"audio/{key}.wav")
            _sock.send(json.dumps({"result": "END"}))
            return

        if not s:
            continue
        _sock.send(json.dumps({"result": "OK", "string": s}, ensure_ascii=False))


if __name__ == "__main__":
    app.run("0.0.0.0", 8000, debug=True)
