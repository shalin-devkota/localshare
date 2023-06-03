from flask import Flask, request, render_template, redirect, send_file
from dbhandler import check_for_data, update_or_add
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def check_for_file(ip):
    file_path = os.path.join(UPLOAD_FOLDER, ip)
    if not os.path.exists(file_path):
        return False
    else:
        return True


@app.route("/", methods=["GET", "POST"])
def home():
    req_addr = request.remote_addr
    if request.method == "POST":
        new_data = request.form.get("new_data")
        update_or_add(req_addr, new_data)
        user_file = request.files["file"]

        sub_folder = os.path.join(app.config["UPLOAD_FOLDER"], req_addr)
        if not os.path.exists(sub_folder):
            os.makedirs(sub_folder)

        if user_file.filename != "":
            filename = secure_filename(user_file.filename)
            user_file.save(os.path.join(sub_folder, filename))

        return redirect("/")
    data = check_for_data(req_addr)
    file_flag = check_for_file(req_addr)

    if data or file_flag:
        context = {}
        file_path = os.path.join(UPLOAD_FOLDER, req_addr)
        if os.path.exists(file_path):
            file_list = [file for file in os.listdir(file_path)]
            if len(file_list) > 0:
                context["file_list"] = file_list
        if data:
            context["data"] = data[0]

        return render_template("data_show.html", **context)
    else:
        return render_template("data_add.html")


@app.route("/download/<filename>")
def download_file(filename):
    req_addr = request.remote_addr
    file_path = os.path.join(UPLOAD_FOLDER, req_addr, filename)
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
