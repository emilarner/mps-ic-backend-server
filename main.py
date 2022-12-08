import requests
import json
import time

from datetime import datetime
from flask import Flask, request, Response

import infinitecampus

MINUTE = 60  # in seconds
TOKEN_EXPIRY = 3 * MINUTE


def get_current_timedate() -> str:
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  return dt_string


def status_message(msg: str):
  print(f"[{get_current_timedate()}]: {msg}")

class Token:

    def __init__(self, token, timestamp = None):
        self.token = token

        # Generate the timestamp
        if (timestamp == None):
            self.timestamp = self.now()
        else:
            self.timestamp = timestamp

    def now(self) -> int:
        return round(time.time())

    def expired(self) -> bool:
        return (self.now() >= (self.timestamp + TOKEN_EXPIRY))


token_cache = {
  
}

app = Flask(__name__)

FUCK_CORS = {'Access-Control-Allow-Origin': '*'}

@app.route("/", methods = ["GET"])
def homepage():
  resp = Response(
    "<h1>Infinite Campus MPS Backend Up!</h1>",
    status = 200,
    mimetype = "text/html",
    headers = FUCK_CORS
  )

  return resp

def username_password_hash(username, password):
  return f"{username}{password}"

@app.route("/login/", methods=["POST"])
def login():
    inputs: dict = request.get_json(force=True)

    # If the args required are not given.
    if ("username" not in inputs or "password" not in inputs):
        return Response("Args missing", status = 500)

    # Login credentials.
    username: str = inputs["username"]

    
    status_message(f"{username} accessed IC integration.")
  
    password: str = inputs["password"]

    uphash = username_password_hash(username, password)

    resp = None

    # If token is stored in cache.
    if (uphash in token_cache):
      token: Token = token_cache[uphash]

      # If it's not expired, send it back
      if (not token.expired()):
        resp = token.token
        return Response(resp, status=200, mimetype="text/plain", headers=FUCK_CORS)

    # If it didn't exist or was expired, generate a new one.    
    resp = infinitecampus.login(username, password)

    # Incorrect credentials
    if (resp == None):
        return Response("0", status=200, mimetype="text/plain", headers=FUCK_CORS)
      
  
    token_cache[uphash] = Token(resp)

    return Response(resp, status=200, mimetype="text/plain", headers=FUCK_CORS)


@app.route("/get-classes/<username>/", methods=["POST"])
def get_classes(username):
    token: str = request.get_json(force=True)["token"]
    return Response(infinitecampus.get_classes(token),
                    mimetype="text/plain",
                    headers=FUCK_CORS)


@app.route("/get-grades/<class_id>/", methods=["POST"])
def get_grades(class_id):
    token: str = request.get_json(force=True)["token"]
    resp = Response(infinitecampus.get_crits_and_grades(token, class_id),
                    status=200,
                    mimetype="text/plain",
                    headers=FUCK_CORS)

    return resp


@app.route("/get-multiple-grades/<assign_id>/", methods=["POST"])
def get_multiple_grades(assign_id):
    try:
        token: str = request.get_json(force = True)["token"]
        response_ic = infinitecampus.get_multiple_grades(token, assign_id)

        resp = Response(response_ic,
                        status=200,
                        mimetype="text/plain",
                        headers=FUCK_CORS)

        return resp
    except Exception as err:
        print(str(err))


if (__name__ == "__main__"):
    print("probably need root to run as port 80")
    app.run(host='0.0.0.0', port=80)