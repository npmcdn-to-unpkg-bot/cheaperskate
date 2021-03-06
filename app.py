import json
from flask import Flask, url_for, redirect, session, render_template, jsonify, request
from flask_oauth2_login import GoogleLogin
from server.plaid_client import PlaidClient
from server.calculator import Calculator
import os

app = Flask(__name__)

app.config.update(
  SECRET_KEY="Miengous3Xie5meiyae6iu6mohsaiRae",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
  GOOGLE_LOGIN_CLIENT_ID="209287169959-bbi3v6tpu99cb65ooos77c07gvmc7m4e.apps.googleusercontent.com",
  GOOGLE_LOGIN_CLIENT_SECRET="BTlujArOQlOc01RXeoIpFbML"
)

google_login = GoogleLogin(app)
plaid_client = PlaidClient("/Users/timyousaf/plaid.txt")
chart_config = json.load(open("static/config.json"))
calculator = Calculator(chart_config)

@app.route("/charts")
def charts():
    print google_login.session()
    return render_template('charts.html')

@app.route("/config")
def config():
    return json.dumps(chart_config)

@app.route("/data")
def data():
    bucket = request.args.get('bucket', "M")
    days_ago = int(request.args.get('days_ago', 730))
    response = calculator.computeChartFromTransactions(plaid_client.getTransactions(), bucket, days_ago)
    return json.dumps(response)

@app.route("/")
def index():
  return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

@google_login.login_success
def login_success(token, profile):
  return jsonify(token=token, profile=profile)

@google_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))

app.run(debug=True)