import json
from model.llm import make_gpt_call


def get_extract_details_prompt(data):
    return f"""
    **Objective:**  
    Extract key details about the bank statement owner from the given key-value pairs.

    ### Input Data:
    {data}

    ### Required Output Format:
    The extracted information **must** be returned in a structured JSON format with the following **mandatory key**:
    - "Starting Account Balance": Extract the initial balance from the statement. If unavailable, default to an empty string (`""`). Ensure the extracted balance is strictly numeric (e.g., `1173.56`). The starting balance is typically mentioned after the statement's opening date like: 'Balance on 01 September 2019' or explicitly labeled as 'Starting Account Balance'.
    - `"Currency"`: The currency used in the bank statement. Represent the currency in short form like: AUD, INR etc. If not found, set it as a USD.

    Additionally, extract and include any other relevant information such as:
    - `"Name"`: The account holder's name.
    - `"Address"`: The account holder's address.
    - `"Phone Number"`: The contact number (if available).
    - `"Account Number"`: The bank account number.
    - `"Bank Name"`: The name of the bank (if present).

    ### Example Output:
        {{
            "Name": "John Doe",
            "Address": "123 Main St, New York, NY",
            "Phone Number": "123-456-7890",
            "Account Number": "9876543210",
            "Bank Name": "XYZ Bank",
            "Starting Account Balance": "1173.56",
            "Currency": "GBP",
        }}

    **IMPORTANT:** Return only the JSON output and nothing else.
    """
def strip_code_fences(response_str):
    if not isinstance(response_str, str):
        response_str = str(response_str)
    response_str = response_str.strip()
    if response_str.startswith("```"):
        start_index = response_str.find("{")
        response_str = response_str[start_index:]
    if response_str.endswith("```"):
        end_index = response_str.rfind("}") + 1
        response_str = response_str[:end_index]
    
    return response_str

def extract_details(table):
    DETAILS_EXTRACTION_PROMPT = get_extract_details_prompt(table)
    transactions = make_gpt_call(DETAILS_EXTRACTION_PROMPT)   
    transactions = strip_code_fences(transactions)
    try:
        transactions_dict = json.loads(transactions.strip())
        if isinstance(transactions_dict, dict):
            return transactions_dict
    except json.JSONDecodeError:
        pass 
    return {"Starting Account Balance": None}

    