import pandas as pd


def extract(result):
    key_value_data = ''
    tabular_data = []
    line_data = '' 
    
    for page in result.pages:
        for line in page.lines:
            line_data += f"Line: {line.content}"

    for kvp in result.key_value_pairs:
        key = kvp.key.content if kvp.key else "N/A"
        value = kvp.value.content if kvp.value else "N/A"
        key_value_data += f"Key: {key}, Value: {value} \n"
    
    for table in result.tables:
        table_data = []
        row_data = []
        r = 0 
        for cell in table.cells:
            if not cell.row_index == r:
                table_data.append(row_data)
                row_data = []
                r += 1
            row_data.append(cell.content)

        if not row_data == []:
            table_data.append(row_data)
        tabular_data.append(pd.DataFrame(table_data))
    
    return line_data, key_value_data, tabular_data