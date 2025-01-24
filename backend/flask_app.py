from flask import Flask # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
from ast import literal_eval

import fenigma_api

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run()

# wedding api routes

@app.route("/fenigma-api/search/<string>")
def search(string):
    try:
      points = literal_eval(f"[{string}]")
      point1 = points[0]
      point2 = points[1]
    except:
      print("YIKES!")
      return "{}"

    return fenigma_api.get_destinations(point1, point2)


@app.route("/")
def home_page():
   return("homepage is functioning as expected.")