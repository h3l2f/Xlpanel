#type: ignore
from __main__ import *

@app.errorhandler(HTTPException)
def HTTPError(e):
    return render_template("HTTPerror.html",errorCode=str(e.code), errorName=e.name, errorDes = e.description), int(e.code)