from model.llm import make_gemini_call, make_gpt_call

def get_has_column_names_prompt(table):
    return f'''
    **Objective:**  
    Determine if the provided table contains identifiable column headers.  
    
    **Input Table:**  
    {table}
    
    **Output Criteria:**  
    - Return **"YES"** if the table includes clear column headers.
    - Return **"NO"** if no column headers are present.
    
    Provide only "YES" or "NO" as the response.
    '''

def get_has_transaction_prompt(table):
    return f"""
    **Objective:**  
    Analyze the provided table and determine if it contains **financial transaction data** i.e. list of transactions. 
    
    **Input Table:**  
    {table}
    
    **Criteria for Identifying Financial Transactions:**  
    1. The table must include columns or data resembling:
       - **Dates**: Indicating when a transaction occurred.
       - **Descriptions**: Providing details or purposes of the transactions.
       - **Amounts**: Numeric values representing money (e.g., credits, debits, balances).
    
    2. Ignore tables that:
       - Contain only general text, metadata, or unrelated content.
       - Do not have numeric values indicative of financial amounts.

    3. Look for clues like column names and values in the rows to identify if the table contains a list of transactions.

    **Response Format:**  
    - If the table contains financial transaction data, return **"Yes"**.  
    - If the table does not contain financial transaction data, return **"No"**.  
    - Provide no additional text or explanation beyond "Yes" or "No".
    """

def gpt_yes_no_check(prompt):
    return make_gpt_call(prompt).strip().lower() == "yes"

def has_column_names(table):
    return gpt_yes_no_check(get_has_column_names_prompt(table))

def has_transactions(table):
    return gpt_yes_no_check(get_has_transaction_prompt(table))