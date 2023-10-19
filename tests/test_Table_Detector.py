import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))
from table_processing.Table_Detector import Table_Detector


@pytest.fixture
def run_Table_Detector_to_excel():
    if os.path.exists("all_excel.xlsx"):
        os.remove("all_excel.xlsx")
    table_detector = Table_Detector(filename = "tests/resources/multipletab.pdf")
    table_detector.to_excel()
    yield os.path.exists("all_excel.xlsx")
    os.remove("all_excel.xlsx")


def test_to_excel():
    assert run_Table_Detector_to_excel


variable_names = "column, row"
values = [(0,list(range(0,10))),
                 (1,list(range(0,10))), 
                 (2,list(range(0,10))), 
                 (3,list(range(0,10))), 
                 (4,[2,3,5,7,9])]


@pytest.fixture
def true_table():
    import pandas as pd
    t_name = 'test_extract_table_content'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx', dtype=str)
    yield trueT


@pytest.fixture
def read_table():
    from table_processing.Table import Table
    t_name = 'test_extract_table_content'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    detc_table = Table_Detector(file_path+'.pdf')
    table = detc_table.get_page_data()[0]['tables'][0]['table_content']
    readT = Table.get_as_dataframe(table)
    yield readT


@pytest.mark.parametrize(variable_names, values)
def test_extract_table_content(column, row, true_table, read_table):
    assert len(true_table) == len(read_table)  # matching row amount
    assert len(true_table.columns.values) == len(read_table.columns.values)  # matching column amount
    for r in row:
        assert str(true_table.iloc[r,column]) == str(read_table.iloc[r,column])  # matching cell contents