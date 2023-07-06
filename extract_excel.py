import openpyxl

def read_excel_to_array(file_path, sheet_name):
    # Load the workbook using openpyxl
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    
    # Select the specific sheet by name
    sheet = workbook[sheet_name]
    
    # Convert the sheet data into a list of lists
    array = []
    for row in sheet.iter_rows(values_only=True):
        evaluated_row = []
        for cell in row:
            if isinstance(cell, str) and cell.startswith('='):
                # Evaluate the formula and append the result
                evaluated_row.append(sheet[cell.coordinate].value)
            else:
                evaluated_row.append(cell)
        array.append(evaluated_row)
    
    return array

# Specify the file path and sheet name of the Excel file
# file_path = 'holding\Income and Expenditure(1).xlsx'
# sheet_name = 'Sheet1'

# Call the function to read the Excel file into an array
# excel_array = read_excel_to_array(file_path, sheet_name)

# Print the array
# print(excel_array)