# type: ignore
from __main__ import *

from flask import make_response, redirect, request

@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (check[0]):
            return redirect("/dashboard")
        return render_template("login.html", name=name)
    else:
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        check = helper.login(user, passwd)
        if check[0]:
            resp = make_response(redirect("/dashboard/"))
            resp.set_cookie("sid",check[1],86400*15,path="/")
            return resp
        else:
            return render_template("login.html", name=name, error=check[1])