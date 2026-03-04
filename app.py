# Import libraries
from flask import Flask, request, render_template, jsonify, redirect, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date":"12/05/2002" , "amount": 100.0},
    {"id": 2, "date":"12/06/2002" , "amount": 50.0}
]

# Read operation
@app.route('/', methods=['GET'])
@app.route('/read', methods=['GET'])
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Show create form
@app.route('/create', methods=['GET'])
def show_create_form():
    return render_template('form.html')

# Create operation (POST)
@app.route('/create', methods=['POST'])
def create_transaction():
    new_id = max([t['id'] for t in transactions], default=0) + 1
    new_transaction = {
        'id': new_id,
        'date': request.form['date'],
        'amount': float(request.form['amount'])
    }
    transactions.append(new_transaction)
    return redirect(url_for('get_transactions'))

# Show update form
@app.route('/update/<int:transaction_id>', methods=['GET'])
def show_update_form(transaction_id):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    return render_template('edit.html', transaction=transaction)

# Update operation (POST)
@app.route('/update/<int:transaction_id>', methods=['POST'])
def update_transaction(transaction_id):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    transaction['date'] = request.form['date']
    transaction['amount'] = float(request.form['amount'])
    return redirect(url_for('get_transactions'))

# Delete operation
@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != transaction_id]
    return redirect(url_for('get_transactions'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 
