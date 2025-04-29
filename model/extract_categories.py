from model.llm import make_gpt_call

def get_prompt(transactions):
    return f"""
    You are an intelligent financial assistant with expertise in transaction categorization.

    Your task is to **analyze each transaction description and assign exactly one financial category per transaction**.  
    **Accuracy is critical, as misclassification can lead to serious financial errors.**  

    ### **Guidelines:**
    - **Every transaction must be assigned exactly one category. The number of categories in the output must be equal to the number of transactions provided.**
    - **Do not generate extra categories, and do not miss any transactions.**
    - Use available clues such as merchant names, keywords, and context to determine the best category.
    - If a transaction could belong to multiple categories, select the most relevant one based on common financial categorization.

    ### **Financial Categories:**
    - **Groceries** (e.g., Walmart, Whole Foods, Trader Joe's)
    - **Salary** (e.g., Payroll, Direct Deposit, Paycheck)
    - **Utilities** (e.g., Electricity, Water, Internet, Gas)
    - **Dining** (e.g., Restaurants, Fast Food, Coffee Shops)
    - **Shopping** (e.g., Amazon, eBay, Retail Stores)
    - **Entertainment** (e.g., Netflix, Movie Tickets, Concerts)
    - **Transport** (e.g., Uber, Lyft, Gas Stations, Public Transport)
    - **Healthcare** (e.g., Hospital, Pharmacy, Insurance)
    - **Rent** (e.g., Apartment Payment, Housing Rent)
    - **Cashback & Rewards** (e.g., Credit Card Cashback, Reward Points Redemption)
    - **Loans & Repayments** (e.g., Mortgage Payment, Personal Loan EMI, Student Loan Payment)
    - **Bank Transfer** (e.g., Any transaction indicating fund transfer between bank accounts)
    - **Electronic Withdrawal** (e.g., Any direct debit, ACH, or auto-deducted payment)

    ### **Example:**
    **Input:**
    ```
    ["PARK FOOD AND WINE CD 7420", "NACH/TP ACH Bajaj Finanac/97127969", "Electronic Withdrawal REF=172890065018740N00", "Transfer to other Bank NetBank Oronsay"]
    ```

    **Output:**
    ```
    Groceries, Loans & Repayments, Electronic Withdrawal, Bank Transfer
    ```

    ### **List of Transaction Descriptions:**
    {transactions}

    ### **Final Instructions:**
    - **Return only the comma-separated list of categories in the same order as the given transactions.**
    - **Ensure that the number of categories exactly matches the number of transactions.**
    - **Do not return any explanations, extra words, or formatting. Return only the list.**

    """

def extract_categories_from_dataframe(transactions):
    CATEGORY_EXTRACTION_PROMPT = get_prompt(transactions['Description'])
    categories = make_gpt_call(CATEGORY_EXTRACTION_PROMPT)
    categories_list = categories.split(',')
    categories_list = ["Other" if cat.strip().lower() in {"uncategorized", "unknown"} else cat.strip() for cat in categories_list]
    return categories_list