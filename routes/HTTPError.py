#type: ignore
from __main__ import *

@app.errorhandler(HTTPException)
def HTTPError(e):
    return render_template("HTTPerror.html", bcolor = bcolor, tcolor = tcolor, pcolor = pcolor, errorCode=str(e.code), errorName=e.name, errorDes = e.description), int(e.code)