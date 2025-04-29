import pandas as pd
import time

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from model.constants import ENDPOINT, FORM_RECOGNIZER_API_KEY
from model.extract_categories import extract_categories_from_dataframe
from model.extract_transactions import extract_transactions
from model.extract_pdf import extract
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from model.table_validator import has_column_names, has_transactions
from tabulate import tabulate

document_analysis_client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(FORM_RECOGNIZER_API_KEY))


def assign_categories(df):
    max_retries = 3
    attempt = 0
    while attempt <= max_retries:
        try:
            categories_list = extract_categories_from_dataframe(df)
            if len(categories_list) == len(df):
                df['Category'] = categories_list
                return df  
            else:
                raise ValueError("Mismatch between the number of categories and DataFrame rows.")

        except ValueError as e:
            print(f"Attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                print("Max retries reached. Unable to assign categories correctly.")  
                df['Category'] = 'Other'
                return df
            else:
                time.sleep(1) 
                attempt += 1

def parse_pdf(pdf_path):
    print('Begin Parsing the pdf..')
    reader = PdfReader(pdf_path)
    last_table_columns = None
    final_df = pd.DataFrame(columns=["Date", "Description", "Credit", "Debit", "Category"])
    data = []
    for page_num in range(len(reader.pages)):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])
        output_pdf_stream = BytesIO()
        writer.write(output_pdf_stream)
        output_pdf_stream.seek(0) 
        poller = document_analysis_client.begin_analyze_document("prebuilt-document", output_pdf_stream)
        result = poller.result()
        line_data, key_value_data, tabular_data = extract(result)
        if page_num == 0:
            data.append({'First page details': line_data})
        data.append(key_value_data)
        for table in tabular_data:
            if has_transactions(table):
                if not has_column_names(table):
                    if last_table_columns is not None:
                        table = pd.concat([pd.DataFrame([last_table_columns], columns=table.columns), table], ignore_index=True)
                        table.reset_index(drop=True, inplace=True)
                    else:
                        continue 
                df = extract_transactions(table) 
                df = assign_categories(df)
                if not df.empty:
                    df = df[["Date", "Description", "Credit", "Debit", "Category"]]  
                    final_df = pd.concat([final_df, df], ignore_index=True)  
                print(tabulate(df, headers='keys', tablefmt='grid'))
                last_table_columns = table.iloc[0]
        print(f"Finished processing page {page_num + 1}")
    return final_df, data