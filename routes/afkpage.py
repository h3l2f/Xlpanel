# type: ignore
from __main__ import *
import time

@app.route("/afk/", methods=["GET"])
def _afk():
    if request.method == "GET":
        beginT = time.time()
        check = helper.chSID(request.cookies.get("sid"))
        if (not check[0]):
            return redirect("/login")
        uDt = helper.checkPteroUser(check[1]["user"])
        if (uDt[0] == False):
            return f"""Something went wrong!\n\nuDt response:\n{uDt}"""

        return render_template(
            "afk.html",
            name=name,
            isAdmin=uDt[1].get("root_admin",False),
            user=check[1]["user"],
            mIt=menuItems,
            coin=check[1]["coin"],
            loadTime=int((time.time()-beginT)*100000)/100000
        )