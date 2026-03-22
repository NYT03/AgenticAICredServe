def verify_transactions(data):
    transactions = data["transactions"]

    balance = transactions[0]["balance"]

    for t in transactions[1:]:
        balance = balance - t["debit"] + t["credit"]

    return round(balance, 2) == round(transactions[-1]["balance"], 2)