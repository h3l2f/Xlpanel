# type: ignore
from __main__ import *

from flask import redirect, request

@app.route("/register/", methods=["GET","POST"])
def register():
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (check[0]):
            return redirect("/dashboard")
        return render_template("register.html", tcolor = tcolor, pcolor = pcolor, bcolor = bcolor, name=name)
    else:
        user = request.form.get("user")
        passwd = request.form.get("passwd")
        cpasswd = request.form.get("cpasswd")
        email = request.form.get("email")
        
        if (not helper.chMX(email.split("@")[::-1][0])) and (config["mail"]["verifyUser"]):
            return render_template(
                "register.html",
                name=name,
                pcolor = pcolor,
                bcolor = bcolor,
                tcolor = tcolor,
                error="Invalid email domain.<br>Is that your real email?",
                user=user
                )
        elif passwd != cpasswd:
            return render_template(
                "register.html",
                name=name,
                error="Something went wrong.",
                user=user,
                pcolor = pcolor,
                bcolor = bcolor,
                tcolor = tcolor,
                email=email
                )
        else:
            check = helper.register(user, passwd, email, dft["cpu"], dft["ram"], dft["disk"], dft["slot"], dft["coin"])
            if not check[0]:
                return render_template(
                    "register.html",
                    name=name,
                    error=check[1],
                    pcolor = pcolor,
                    bcolor = bcolor,
                    tcolor = tcolor,
                    email=email if "User" in check[1] else "",
                    user=user if "Email" in check[1] else ""
                    )
            else:
                return redirect("/login")