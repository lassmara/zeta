from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy function for classifying disputes based on description
def classify_dispute(description):
    if "fraud" in description.lower():
        return "Fraud"
    elif "chargeback" in description.lower():
        return "Chargeback"
    elif "billing" in description.lower():
        return "Billing Error"
    else:
        return "Duplicate Transaction"

# Dummy function to assign priority based on customer history
def assign_priority(customer_history):
    if customer_history.get('frequent_disputes', 0) > 5:
        return "High"
    elif customer_history.get('total_spent', 0) > 1000:
        return "Medium"
    return "Low"

@app.route('/submit_dispute', methods=['POST'])
def submit_dispute():
    data = request.get_json()
    dispute_description = data.get('dispute_description')
    customer_history = data.get('customer_history')

    # Step 1: Classify the dispute
    dispute_type = classify_dispute(dispute_description)

    # Step 2: Assign priority based on customer history
    priority = assign_priority(customer_history)

    # Step 3: Recommend action based on classification
    if dispute_type == "Fraud":
        action = "Send to Fraud Detection Team"
    elif dispute_type == "Chargeback":
        action = "Send to Chargeback Team"
    elif dispute_type == "Billing Error":
        action = "Send to Billing Team"
    else:
        action = "Send to Transaction Reconciliation Team"

    return jsonify({
        'dispute_type': dispute_type,
        'priority': priority,
        'recommended_action': action,
        'status': 'Dispute received and routed successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)
