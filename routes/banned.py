#type: ignore
from __main__ import *

@app.route("/banned/")
def _bn():
    return render_template("banned.html")