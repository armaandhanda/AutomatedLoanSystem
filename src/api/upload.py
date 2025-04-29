import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
from model.main import process_pdf

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}})  

# def process_pdf(pdf, a, b):
#     return {
#     "user_summary": {
#         "Name": "Oleh Beshleu",
#         "Address": "293 STRONE ROAD, MANOR PARK (BARKING AND DAGENHAM), LONDON, E12 6TR",
#         "Account Number": "45201526",
#         "Bank Name": "LLOYDS BANK"
#     },
#     "financial_summary": {
#         "Starting Balance": "1173.56",
#         "Ending Balance": "2792.20",
#         "Total Credit": "5420.12",
#         "Total Debit": "3801.48",
#         "Total Savings": "1618.64"
#     },
#     "monthly_summary": [
#         {"Month": "September", "Net_Credit": 1010.0, "Net_Debit": 1070.11, "Net_Savings": -60.11, "Cumulative_Savings": -60.11},
#         {"Month": "October", "Net_Credit": 2380.0, "Net_Debit": 546.78, "Net_Savings": 1833.22, "Cumulative_Savings": 1773.11},
#         {"Month": "November", "Net_Credit": 2030.12, "Net_Debit": 2184.59, "Net_Savings": -154.47, "Cumulative_Savings": 1618.64}
#     ],
#     "credit_distribution": [
#         {"Category": "Electronic Withdrawal", "total_credit": 3480.0},
#         {"Category": "Shopping", "total_credit": 1740.0},
#         {"Category": "Transport", "total_credit": 200.12}
#     ],
#     "debit_distribution": [
#         {"Category": "Dining", "total_debit": 325.63},
#         {"Category": "Electronic Withdrawal", "total_debit": 210.0},
#         {"Category": "Groceries", "total_debit": 1479.21},
#         {"Category": "Healthcare", "total_debit": 33.03},
#         {"Category": "Shopping", "total_debit": 926.18},
#         {"Category": "Transport", "total_debit": 777.43},
#         {"Category": "Utilities", "total_debit": 50.0}
#     ],
#     "existing_loans": [{'Description': 'NACH/TP ACH Bajaj Finanac/88551679', 'Type': 'Loan', 'Amount': 1912.0}, {'Description': 'POSVISA/KARUN MEDICAL/809414290216', 'Type': 'Reoccurring Payment', 'Amount': 75.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDAN I AKRUTI/...', 'Type': 'Reoccurring Payment', 'Amount': 500.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDAN I AKRUTI/...', 'Type': 'Reoccurring Payment', 'Amount': 1000.0}, {'Description': 'NACH/TP ACH Bajaj Finanac/97127969', 'Type': 'Loan', 'Amount': 1912.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDANI AKRUTI/8150194', 'Type': 'Reoccurring Payment', 'Amount': 500.0}, {'Description': 'POSVISA/KARUN MEDICAL/814016444557', 'Type': 'Reoccurring Payment', 'Amount': 75.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDANI AKRUTI/8150191', 'Type': 'Reoccurring Payment', 'Amount': 1000.0}, {'Description': 'NACH/TP ACH Bajaj Finanac/101294174', 'Type': 'Loan', 'Amount': 1912.0}, {'Description': 'Charge: Cash Wdl at other ATM/Inv270 518151366', 'Type': 'Reoccurring Payment', 'Amount': 20.0}, {'Description': 'CGST on Charge: Cash Wdl at other ATM/Inv2705', 'Type': 'Reoccurring Payment', 'Amount': 1.8}, {'Description': 'SGST on Charge: Cash Wdl at other ATM/Inv2705', 'Type': 'Reoccurring Payment', 'Amount': 1.8}, {'Description': 'NACH/TP ACH Bajaj Finanac/108265552', 'Type': 'Reoccurring Payment', 'Amount': 1912.0}, {'Description': 'POSVISA/KARUN MEDICAL/818406584956', 'Type': 'Reoccurring Payment', 'Amount': 75.0}, {'Description': 'POSVISA/KARUN MEDICAL/822706734149', 'Type': 'Reoccurring Payment', 'Amount': 75.0}, {'Description': 'POSVISA/KARUN MEDICAL/824405792484', 'Type': 'Reoccurring Payment', 'Amount': 75.0}, {'Description': 'NACH/TP ACH Bajaj Finanac/122175597', 'Type': 'Reoccurring Payment', 'Amount': 1912.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDAN I AKRUTI', 'Type': 'Reoccurring Payment', 'Amount': 500.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDAN I AKRUTI/8...', 'Type': 'Reoccurring Payment', 'Amount': 1000.0}, {'Description': 'ATMNFS/CASH WITHDRAWAL/+HIRANANDAN I AKRUTI/8...', 'Type': 'Reoccurring Payment', 'Amount': 500.0}, {'Description': 'Charge: Cash Wdl at other ATM/Inv271 018190582...', 'Type': 'Reoccurring Payment', 'Amount': 20.0}, {'Description': 'CGST on Charge: Cash Wdl at other AT M/Inv2710...', 'Type': 'Reoccurring Payment', 'Amount': 1.8}],
#     "verdict": """The decision on the loan application for GBP 9.4 is as follows:
    
# **Decision: Approved**

# **Explanation:** The individual displays sound financial management as evidenced by their substantial ending balance of GBP 2792.20 and net positive savings over the last three months, resulting in a cumulative savings of GBP 1618.64. Furthermore, the total credit significantly exceeds the total debit, indicating a positive cash flow trend. Given the requested loan amount is relatively small (GBP 9.40), and there are no existing loans, the individual seems to have sufficient financial capacity to repay the loan."""
# }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf = request.files['file']
    loan_currency = request.form.get("loan_currency")
    loan_amount = float(request.form.get("loan_amount"))
    response_data = process_pdf(pdf, loan_amount, loan_currency)
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
