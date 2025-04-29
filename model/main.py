import pandas as pd

from model.constants import conversion_chart
from model.extract_details import extract_details
from model.finding_loans import find_loans
from model.generate_summary import get_summary
from model.generate_verdict import generate_verdict
from model.parser import parse_pdf


def clean_and_format_transactions(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m', errors='coerce')
    df['Credit'] = df['Credit'].str.replace(',', '', regex=True)
    df['Debit'] = df['Debit'].str.replace(',', '', regex=True)
    df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce')
    df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce')
    df = df.dropna(subset=['Date', 'Credit', 'Debit'])
    df['Month'] = df['Date'].dt.strftime('%B')  
    df['Sequential_Month'] = (df['Month'] != df['Month'].shift()).cumsum()  
    return df

def aggregate_transactions_by_category(df_transactions):
    df_credit = df_transactions[df_transactions['Credit'] > 0]
    df_debit = df_transactions[df_transactions['Debit'] > 0]
    credit_distribution = df_credit.groupby('Category')['Credit'].sum().reset_index(name='total_credit')
    debit_distribution = df_debit.groupby('Category')['Debit'].sum().reset_index(name='total_debit') 
    return credit_distribution, debit_distribution

def convert_loan_amount(amount, loan_currency, bank_statement_currency):
    if loan_currency == bank_statement_currency:
        return amount  
    conversion_factor = conversion_chart.get((loan_currency, bank_statement_currency))
    converted_amount = amount * conversion_factor
    return converted_amount
  

def process_pdf(pdf, loan_amount = 1000, loan_currency = 'EUR'):
    df_transactions, data  = parse_pdf(pdf)
    df_transactions = clean_and_format_transactions(df_transactions)
    details = extract_details(data)
    bank_statement_currency = details.pop("Currency", "USD")  
    loan_amount = convert_loan_amount(loan_amount, loan_currency, bank_statement_currency)
    credit_distribution, debit_distribution = aggregate_transactions_by_category(df_transactions)
    user_summary, financial_summary, monthly_summary = get_summary(df_transactions, details)
    existing_loans = find_loans(df_transactions)
    verdict = generate_verdict(monthly_summary, financial_summary, debit_distribution, existing_loans, loan_amount, bank_statement_currency)
    response_data = {
        "user_summary": user_summary,
        "financial_summary": financial_summary,
        "monthly_summary": monthly_summary.to_dict(orient="records"),
        "credit_distribution": credit_distribution.to_dict(orient="records"),
        "debit_distribution":  debit_distribution.to_dict(orient="records"),
        "existing_loans": existing_loans.to_dict(orient="records"),
        "verdict": verdict
    }
    print(f'The response data is: {response_data}')
    return response_data


#process_pdf('/Users/anuragmudgil/Desktop/Study/Casca/examples/example_5.pdf')