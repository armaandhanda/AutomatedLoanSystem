import pandas as pd
from model.llm import make_gemini_call, make_gpt_call

def get_prompt(table):
    return f"""    
    **Objective:**  
    Extract all transaction data from the provided table and format it into a structured output. 
    Ensure that each transaction and its corresponding details are accurately captured without any omissions.

    **Input Table:**  
    {table}

    **Instructions for Extraction:**  
    1. Extract and organize the data into the following columns:
       - **Date**: Convert all dates to the format DD/MM. 
       - **Description**: Include the purpose or details of the transaction as presented in the table.
       - **Credit**: Record money received (inflow).
       - **Debit**: Record money spent (outflow).

    2. Ignore any rows or entries that do not contain valid transaction information.

    3. Ensure the output table adheres to the following format:
       ```
       | Date      | Description | Credit | Debit |
       |-----------|-------------|--------|-------|
       | 01/01/23 | Salary      | 1000   | 0     |
       | 05/01/24 | Groceries   | 0      | 200   |
       | 10/01/25 | Rent        | 0      | 500   |
       ```
    
    **Output Requirements:**  
    - The output should consist of only the structured table with the column names: `Date`, `Description`, `Credit`, and `Debit`.
    - Replace any missing values in the `Credit` or `Debit` columns with `0`.

    **Note:**  
    - Be consistent in formatting and avoid introducing any extraneous content or commentary.
    - Retain the order of transactions as they appear in the original table.
    """

def convert_to_dataframe(data):

    data_list = []
    lines =  data.split('\n')
    for line in lines:
        if '|' in line:
            words_list = [word.strip() for word in line.split('|')]
            data_list.append(words_list) 
    if len(data_list) <= 1:
        return pd.DataFrame(columns=["Date", "Description", "Credit", "Debit"])
    df = pd.DataFrame(data_list[1:], columns = data_list[0])
    df["Description"] = df["Description"].str.replace("-", "", regex=False)
    df = df[df["Description"] != ""].reset_index(drop=True)
    return df

def extract_transactions(table):
    TRANSACTION_EXTRACTION_PROMPT = get_prompt(table)
    transactions = make_gpt_call(TRANSACTION_EXTRACTION_PROMPT)
    df = convert_to_dataframe(transactions)
    return df