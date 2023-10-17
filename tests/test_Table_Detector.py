import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


@pytest.fixture
def run_Table_Detector_to_excel():
    from table_processing.Table_Detector import Table_Detector
    if os.path.exists("all_excel.xlsx"):
        os.remove("all_excel.xlsx")
    table_detector = Table_Detector(filename = "tests/resources/test_files/multipletab.pdf")
    table_detector.to_excel()
    yield os.path.exists("all_excel.xlsx")
    os.remove("all_excel.xlsx")


def test_to_excel():
    assert run_Table_Detector_to_excel


def test_extract_table_content():
    import pandas as pd
    from table_processing.Table import Table
    from table_processing.Table_Detector import Table_Detector

    t_name = 'test_extract_table_content'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx', dtype=str)
    detc_table = Table_Detector(file_path+'.pdf')
    table = detc_table.get_page_data()[0]['tables'][0]['table_content']
    readT = Table.get_as_dataframe(table)

    assert len(trueT) == len(readT)  # matching row amount
    assert len(trueT.columns.values) == len(readT.columns.values)  # matching column amount

    correct_cells = {0:list(range(0,10)), 1:list(range(0,10)), 2:list(range(0,10)), 
                     3:list(range(0,10)), 4:[2,3,5,7,9]}
    for c in correct_cells.keys():
        for r in correct_cells[c]:
            assert str(trueT.iloc[r,c]) == str(readT.iloc[r,c])  # matching cell contents
