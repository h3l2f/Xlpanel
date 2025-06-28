# type: ignore
from __main__ import *

from flask import redirect, request

@app.route("/register/", methods=["GET","POST"])
def register():
    cf_site_key = config["cf_turnstile"]["site_key"]
    cf_enable = config["cf_turnstile"]["enable"]
    if request.method == "GET":
        check = helper.chSID(request.cookies.get("sid"))
        if (check[0]):
            return redirect("/dashboard")
        return render_template("register.html", cf_site_key=cf_site_key, cf_enable=cf_enable,   name=name)
    else:
        user = request.form.get("user").replace(" ", "")
        passwd = request.form.get("passwd")
        cpasswd = request.form.get("cpasswd")
        email = request.form.get("email")
        cf_token = request.form.get("cf-turnstile-response")
        cf_ip = request.form.get("CF-Connecting-IP")
        e = helper.cf_check(cf_token, cf_ip)
        if not e[0]:
            return render_template(
                "register.html",
                name=name,
                error="Invalid captcha.",
                user=user,
                email=email,
                cf_site_key=cf_site_key, cf_enable=cf_enable,
                )
        
        if (not helper.chMX(email.split("@")[::-1][0])) and (config["mail"]["verifyUser"]):
            return render_template(
                "register.html",
                name=name,
                error="Invalid email domain.<br>Is that your real email?",
                user=user,
                cf_site_key=cf_site_key, cf_enable=cf_enable,
                )
        elif passwd != cpasswd:
            return render_template(
                "register.html",
                name=name,
                error="Something went wrong.",
                user=user,
                email=email,
                cf_site_key=cf_site_key, cf_enable=cf_enable,
                )
        else:
            check = helper.register(user, passwd, email, dft["cpu"], dft["ram"], dft["disk"], dft["slot"], dft["coin"])
            if not check[0]:
                return render_template(
                    "register.html",
                    name=name,
                    error=check[1],
                    cf_site_key=cf_site_key, cf_enable=cf_enable,
                    email=email if "User" in check[1] else "",
                    user=user if "Email" in check[1] else ""
                    )
            else:
                return redirect("/login")