from table_metrics import test_tables
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy as np

def compare_tables(file1, file2):
    '''
    Compares two Excel files and generates a new Excel file with comparison 
    results of the tables within each sheet. Input should be the file name,
    and Excel files should be stored in use_tools > excel_table_comparison > excel_files.
    Results are generated in use_tools > excel_table_comparison.
    '''
    
    # Import Excel file paths
    file_path_original = './use_tools/excel_table_comparison/excel_files/' + file1 + '.xlsx'
    file_path_comparison = './use_tools/excel_table_comparison/excel_files/' + file2 + '.xlsx'
    original_wb = openpyxl.load_workbook(file_path_original)
    comparison_wb = openpyxl.load_workbook(file_path_comparison)

    # Create a new workbook and worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Summary"
    # Add column titles to the "Summary" sheet
    sheet.append(['Sheet name', '% Correct', 'Overlap', 'String Similarity', 'Completeness', 'Purity', 'Precision', 'Recall'])

    # Initialize list to store % correct values
    percent_correct_list = []

    # Go through each sheet in the comparison workbook
    for sheet_name in comparison_wb.sheetnames:
        if sheet_name in original_wb.sheetnames:
            original_df = pd.read_excel(file_path_original, sheet_name=sheet_name, header=None)
            comparison_df = pd.read_excel(file_path_comparison, sheet_name=sheet_name, header=None)

            # Create a dataframe that contains True where the two tables are equal and False where they are not
            if original_df.shape == comparison_df.shape: # If the two tables are the same size
                differences_df = pd.DataFrame(comparison_df.values == original_df.values, index=original_df.index, columns=original_df.columns)
            else: # If the two tables are different sizes
                if original_df.size > comparison_df.size:   # Determine which dataframe is larger
                    larger_df = original_df
                    smaller_df = comparison_df
                else:
                    larger_df = comparison_df
                    smaller_df = original_df

                new_df = smaller_df_to_larger_df(larger_df, smaller_df)
                
                # Fill NaN values in both DataFrames so they have the same shape
                larger_df_filled = larger_df.fillna('blank')
                new_df_filled = new_df.fillna('blank')

                # Compare the filled DataFrames
                differences_df = pd.DataFrame(larger_df_filled == new_df_filled, index=larger_df.index, columns=larger_df.columns)

            # Write the sheet name to the worksheet
            new_sheet = workbook.create_sheet(title=sheet_name)

            # Write the second table to the worksheet
            if original_df.size > comparison_df.size:
                comparison_df = smaller_df_to_larger_df(original_df, comparison_df)
            rows = dataframe_to_rows(comparison_df, index=False, header=False)
            for row in rows:
                new_sheet.append(row)

            # Format the cells that are different from the original table
            for row in new_sheet.iter_rows(min_row=new_sheet.max_row-len(comparison_df)+1, min_col=1):
                for cell in row:
                    # Check if the cell is different from the original table
                    list_of_rows = differences_df.values
                    if list_of_rows[cell.row-new_sheet.max_row+len(comparison_df)-1, cell.column-1] == False:
                        # If the cell is different, highlight it with yellow
                        cell.fill = openpyxl.styles.PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

            # Calculate the statistics
            num_cells = comparison_df.size
            num_true = differences_df.sum().sum()
            percent_true = differences_df.mean().mean() * 100
            overall_percent_diff = 100 - (num_true / num_cells * 100)

            # Write the statistics to the worksheet
            new_sheet.append([])
            new_sheet.append(['Number of Correct Cells', num_true])
            new_sheet.append(['% Correct', percent_true])
            new_sheet.append(['Number of Incorrect Cells', num_cells - num_true])
            new_sheet.append(['% Different (Incorrect)', overall_percent_diff])
            new_sheet.append([])
            new_sheet.append(['Comparison metrics:'])

            # Calculate comparison metrics using the test_tables function
            metrics_df = test_tables({sheet_name: [original_df,comparison_df]})

            # Write comparison metrics to the Excel file
            rows = dataframe_to_rows(metrics_df, index=False, header=True)
            for row in rows:
                new_sheet.append(row)

            # Write sheet name, % correct, and comparison metrics to "Summary" sheet
            sheet.append([sheet_name, percent_true, metrics_df['Overlap'][0], metrics_df['String Similarity'][0], 
                metrics_df['Completeness'][0], metrics_df['Purity'][0], metrics_df['Precision'][0], metrics_df['Recall'][0]])

            # Append % correct to list
            percent_correct_list.append(percent_true)
        else:
            print(f"{sheet_name} not found in {file1}.xlsx")

    # Calculate statistics for % correct over all sheets
    mean_percent_correct = np.mean(percent_correct_list)
    median_percent_correct = np.median(percent_correct_list)
    min_percent_correct = np.min(percent_correct_list)
    max_percent_correct = np.max(percent_correct_list)
    range_percent_correct = max_percent_correct - min_percent_correct

    # Write statistics for % correct over all sheets to "Main" sheet
    sheet.append([])
    sheet.append(['Summary Statistics:'])
    sheet.append(['Mean (% Correct)', mean_percent_correct])
    sheet.append(['Median (% Correct)', median_percent_correct])
    sheet.append(['Min (% Correct)', min_percent_correct])
    sheet.append(['Max (% Correct)', max_percent_correct])
    sheet.append(['Range (% Correct)', range_percent_correct])

    # Save the workbook to a new file
    save_path = './use_tools/excel_table_comparison/' + file1 + '_and_' + file2 + '_comparison_results.xlsx'
    workbook.save(save_path)

def smaller_df_to_larger_df(larger_df, smaller_df):
                    '''
                    Creates a new dataframe with the same shape as the larger dataframe, and fills it with empty values.
                    Copies the values from the smaller dataframe into the corresponding cells of the new dataframe.
                    '''
                    # Create a new dataframe with the same shape as the larger dataframe, and fill it with empty values
                    new_df = pd.DataFrame(index=larger_df.index, columns=larger_df.columns)

                    # Copy the values from the smaller dataframe into the corresponding cells of the new dataframe
                    new_df.loc[smaller_df.index, smaller_df.columns] = smaller_df.values
                    
                    return new_df

# Get file names from user input
first_file = input("Enter the name of the first Excel file: ")
second_file = input("Enter the name of the second Excel file: ")

# Use the function to compare the files
compare_tables(first_file, second_file)