from model.llm import make_gpt_call

def get_prompt(monthly_summary, financial_summary, debit_distribution, existing_loans, loan_amount, bank_statement_currency):
    return f"""
    You are a loan expert analyzing an individual's financial history. You are provided with their month-to-month net debit and credit, 
    existing loans (if any), and the requested loan amount. Your task is to assess whether they should be approved for a loan. 
    Provide a concise **Decision** (either "Approved" or "Rejected") followed by a **brief 2-3 line explanation** supporting your reasoning.

    **Important Formatting Rules:**
    - Start the output with **Decision: Approved** or **Decision: Rejected**.
    - After that, write **Explanation:** followed by the justification.
    - Ensure the explanation is **brief and professional**, covering key factors like savings, spending patterns, and existing loans.

    ---
    **Currency:** {bank_statement_currency}

    **MONTHLY SUMMARY:**
    {monthly_summary}

    **FINANCIAL SUMMARY:**
    {financial_summary}

    **HOW THE PERSON IS SPENDING THE MONEY:**
    {debit_distribution}

    **EXISTING LOANS:**
    {existing_loans}

    **REQUESTED LOAN AMOUNT:**
    {loan_amount}
    ---
    
    Please provide only the decision and explanation in the format below:
    
    **Example Output:**
    
    Decision: Approved
    Explanation: The individual has a strong financial history with positive net savings. Their credit inflow exceeds debit expenditures, and they have no existing loans. Given the requested loan amount is small, they have sufficient capacity to repay.

    OR

    Decision: Rejected
    Explanation: The individual has high debt relative to their monthly income, and their net savings trend is negative. Additionally, they have existing loans, increasing their financial burden. The requested loan amount is high, making repayment uncertain.
    """

def generate_verdict(monthly_summary, financial_summary, debit_distribution, existing_loans, loan_amount, bank_statement_currency):
    VERDICT_PROMPT = get_prompt(monthly_summary, financial_summary, debit_distribution, existing_loans, loan_amount, bank_statement_currency)
    initial_line = f"The decision on the loan application for {bank_statement_currency} {loan_amount} is as follows:"
    verdict = initial_line + make_gpt_call(VERDICT_PROMPT)
    return verdict