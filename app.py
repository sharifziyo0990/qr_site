from flask import Flask, render_template, request, send_from_directory
import qrcode, os, uuid, time, threading

app = Flask(__name__)

STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

TEMP_LIFETIME = 60  # sekunda, QR keyin avtomatik o'chadi

# Fon thread: eski QR fayllarni o'chiradi
def cleanup_temp_files():
    while True:
        now = time.time()
        for file in os.listdir(STATIC_DIR):
            path = os.path.join(STATIC_DIR, file)
            if os.path.isfile(path) and now - os.path.getmtime(path) > TEMP_LIFETIME:
                try:
                    os.remove(path)
                except:
                    pass
        time.sleep(10)

threading.Thread(target=cleanup_temp_files, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    if request.method == "POST":
        data = request.form.get("data")
        if data:
            qr_filename = f"qrcode_{uuid.uuid4().hex}.png"
            qr_path = os.path.join(STATIC_DIR, qr_filename)
            img = qrcode.make(data)
            img.save(qr_path)
    return render_template("index.html", qr_filename=qr_filename)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(STATIC_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


import os
from flask import Flask, render_template, request, send_from_directory
import qrcode, uuid

app = Flask(__name__)

STATIC_DIR = "static"
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_filename = None
    if request.method == "POST":
        data = request.form.get("data")
        if data:
            qr_filename = f"qrcode_{uuid.uuid4().hex}.png"
            qr_path = os.path.join(STATIC_DIR, qr_filename)
            img = qrcode.make(data)
            img.save(qr_path)
    return render_template("index.html", qr_filename=qr_filename)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(STATIC_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
