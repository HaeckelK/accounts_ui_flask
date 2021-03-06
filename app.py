import json

from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


def get_api_endpoint(path: str):
    response = requests.get(f"http://127.0.0.1:5000/api/v1.0/{path}")
    return response.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bank")
def bank_index():
    bank_account_details = get_api_endpoint("bank_account_details")
    return render_template("bank_index.html", bank_account_details=bank_account_details)


@app.route("/bank/accounts")
def bank_accounts():
    """List out bank accounts"""
    bank_account_details = get_api_endpoint("bank_account_details")
    return render_template("bank_accounts.html", bank_account_details=bank_account_details)


@app.route("/bank/create")
def create_bank_account():
    return """Create bank account via POST to <br>http://127.0.0.1:5000/api/v1.0/bank_accounts
"""


@app.route("/bank_transactions/<bank_account_id>")
def bank_transactions(bank_account_id):
    data = get_api_endpoint(f"bank_transactions/{bank_account_id}")
    account_details = data["account_details"]
    transactions = data["transactions"]
    return render_template("bank_transactions.html", account_details=account_details, transactions=transactions)


@app.route("/categorise_bank_transactions/<bank_account_id>")
def categorise_bank_transactions(bank_account_id):
    if request.args:
        transaction_id = request.args["transaction_id"]
        category = request.args["category"]
        requests.post(f"http://127.0.0.1:5000/api/v1.0/bank_transaction/{transaction_id}", json={"category": category})
        return redirect(url_for("categorise_bank_transactions", bank_account_id=bank_account_id))

    data = get_api_endpoint(f"bank_transactions/{bank_account_id}?uncategorised=1")
    account_details = data["account_details"]
    transactions = data["transactions"]
    return render_template("categorise_bank_transactions.html", account_details=account_details, transactions=transactions)


if __name__ == '__main__':
    app.run(debug=True, port=5001)