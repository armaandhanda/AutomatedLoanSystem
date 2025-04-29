import pandas as pd
import re

def generate_financial_summary(monthly_summary, details):

    starting_balance = details.pop("Starting Account Balance", None)  
    ending_balance = None
    if starting_balance is not None:
        cleaned_balance = re.sub(r"[^\d.]", "", starting_balance)
        ending_balance = float(cleaned_balance) + monthly_summary["Cumulative_Savings"].iloc[-1]
    total_credit = monthly_summary["Net_Credit"].sum()
    total_debit = monthly_summary["Net_Debit"].sum()
    total_savings = monthly_summary["Net_Savings"].sum()    
    financial_summary = {
        "Starting Balance": starting_balance,
        "Ending Balance": f"{ending_balance:.2f}",
        "Total Credit": f"{total_credit:.2f}",
        "Total Debit": f"{total_debit:.2f}",
        "Total Savings": f"{total_savings:.2f}"
    }
    filtered_details =  {key: value for key, value in details.items() if value != ""}
    return financial_summary, filtered_details


def get_monthly_summary(df):
    monthly_summary = df.groupby('Sequential_Month').agg(
        Month=('Month', 'first'),
        Net_Credit=('Credit', 'sum'),
        Net_Debit=('Debit', 'sum')
    )
    monthly_summary['Net_Savings'] = monthly_summary['Net_Credit'] - monthly_summary['Net_Debit']
    monthly_summary['Cumulative_Savings'] = monthly_summary['Net_Savings'].cumsum()
    monthly_summary = monthly_summary.reset_index(drop=True)
    return monthly_summary


def get_summary(df_transactions, details):
    monthly_summary = get_monthly_summary(df_transactions)
    financial_summary, user_summary = generate_financial_summary(monthly_summary, details)
    return user_summary, financial_summary, monthly_summary