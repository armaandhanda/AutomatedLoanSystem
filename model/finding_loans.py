import pandas as pd

def clean_description(desc):
    return ''.join(filter(str.isalpha, desc)).lower() if isinstance(desc, str) else ""

def categorize_transaction(row):
    if "loan" in row["Category"].lower():
        return "Loan"
    elif row["Count"] > 3:
        return "Reoccurring Payment"
    return None 


def find_loans(df):
    df["Cleaned_Description"] = df["Description"].apply(clean_description)
    # Subtraction ensures that duplicate payments are either all credit or all debit
    df["Amount"] = df["Debit"] - df["Credit"]
    duplicate_transactions = df[df.duplicated(subset=["Cleaned_Description", "Amount"], keep=False)]
    if duplicate_transactions.empty:
        return pd.DataFrame(columns=["Description", "Type", "Amount"])
    transaction_counts = duplicate_transactions.groupby(["Cleaned_Description", "Amount"]).size().reset_index(name="Count")
    duplicate_transactions = duplicate_transactions.merge(
        transaction_counts, on=["Cleaned_Description", "Amount"], how="left"
    )
    duplicate_transactions["Type"] = duplicate_transactions.apply(categorize_transaction, axis=1)
    filtered_transactions = duplicate_transactions[duplicate_transactions["Type"].notna()][["Description", "Cleaned_Description", "Type", "Amount"]].drop_duplicates()
    filtered_transactions["Is_Loan"] = filtered_transactions["Type"].eq("Loan")
    filtered_transactions = filtered_transactions.sort_values(
        by="Is_Loan", 
        ascending=False
    )
    unique_filtered_transactions = filtered_transactions.drop_duplicates(
        subset=["Cleaned_Description", "Amount"],
        keep="first"
    )
    unique_filtered_transactions.drop(columns="Is_Loan", inplace=True)  
    # SHowing only the debit ones
    unique_filtered_transactions = unique_filtered_transactions[unique_filtered_transactions["Amount"] > 0]
    return unique_filtered_transactions