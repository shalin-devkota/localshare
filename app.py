from flask import Flask, request, render_template, redirect
from dbhandler import check_for_data, update_or_add

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    req_addr = request.remote_addr
    if request.method == "POST":
        new_data = request.form.get("new_data")
        update_or_add(req_addr, new_data)
        return redirect("/")
    data = check_for_data(req_addr)

    if data:
        return render_template("data_show.html", data=data[0])
    else:
        return render_template("data_add.html")


if __name__ == "__main__":
    app.run(debug=True)
