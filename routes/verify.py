# type: ignore
from __main__ import *

from flask import jsonify, make_response, redirect, request

@app.route("/verify/", methods=["GET","POST"])
def verify():
    if request.method == "GET":
        if not request.args.get("user"): abort(403)
        return render_template("verify.html", name=name)
    else:
        code = request.form.get("code")
        user = request.form.get("user")
        if (not code) or (not user): abort(403)
        check = helper.checkVcode(user, code)
        return jsonify({"status": check[0], "message": check[1]})