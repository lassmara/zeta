from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy function to calculate loan eligibility based on income, loan amount, and credit score
def calculate_loan_eligibility(income, loan_amount, credit_score):
    if income >= loan_amount * 2 and credit_score >= 650:
        return {"eligibility": "Approved", "score": 85, "recommendation": "Loan approved. Proceed with application."}
    elif income >= loan_amount * 1.5 and credit_score >= 600:
        return {"eligibility": "Pending", "score": 70, "recommendation": "Loan pending. Provide additional documentation."}
    else:
        return {"eligibility": "Denied", "score": 40, "recommendation": "Loan denied. Improve your credit score."}

@app.route('/loan_application', methods=['POST'])
def loan_application():
    data = request.get_json()
    income = data.get('income')
    loan_amount = data.get('loan_amount')
    credit_score = data.get('credit_score')

    # Calculate eligibility
    result = calculate_loan_eligibility(income, loan_amount, credit_score)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
