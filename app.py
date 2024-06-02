# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html",transactions=transactions)

# Create operation
@app.route("/add", methods=["GET","POST"])
def add_transaction():
    if request.method == "POST":

        #Create New Transaction
        transaction = {
              'id': len(transactions)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
            }

        #Add Transaction to Transactions
        transactions.append(transaction)

        #Redirect to Home Page
        return redirect(url_for("get_transactions"))

    #If Method is get, render the form page
    return render_template("form.html",)


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET","POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        #Extract The Updated Valued from POST request
        date = request.form['date']
        amount = float(request.form['amount'])
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)    

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

# Search Transactions
@app.route("/search", methods = ["GET","POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        filtered_transactions = []
        for t in transactions:
            if (min_amount <= t['amount'] <= max_amount):
                filtered_transactions.append(t)
        return render_template("transactions.html", transactions = filtered_transactions)
    
    return render_template("search.html")

# Total Balance
@app.route("/balance")
def total_balance():
    balance = 0
    for t in transactions:
        balance += t['amount']
    return render_template("transactions.html",transactions=transactions,
    total_balance = balance)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    