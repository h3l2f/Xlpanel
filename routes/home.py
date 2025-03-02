# type: ignore
from __main__ import *

@app.route("/")
def hp():
    return render_template("index.html")