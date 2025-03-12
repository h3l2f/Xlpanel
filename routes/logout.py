# type: ignore
from __main__ import *

@app.route("/logout/", methods=["GET"])
def lout():
    if request.method == "GET":
        helper.logout(request.cookies.get("sid"))
        return redirect("/login")