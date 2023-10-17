import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


def test_calculate_row_column_limits():
    from table_processing.table_tools import _calculate_row_column_limits,remove_duplicate_limits
    expected_row_limit=[]
    expected_col_limit=[]
    img_dim = (730,250)
    test_bbox = [[122,122.7,133,42],[50,40,123,100],[26,107,108.2,111]]
    for box in test_bbox:
        x1,y1,x2,y2 = box
        expected_row_limit.append(y1)
        expected_row_limit.append(y2)
        expected_col_limit.append(x1)
        expected_col_limit.append(x2)
    
    expected_col_limit.sort()
    expected_row_limit.sort()

    expected_col_limit = remove_duplicate_limits(expected_col_limit,16)
    expected_row_limit = remove_duplicate_limits(expected_row_limit,8)

    expected_col_limit.pop(0)
    expected_col_limit.pop()


    expected_col_limit.append(0)
    expected_col_limit.append(img_dim[0])
    expected_row_limit.append(0)
    expected_row_limit.append(img_dim[1])

    expected_col_limit.sort()
    expected_row_limit.sort()

    returned_col_limit, returned_row_limit = _calculate_row_column_limits(img_dim,test_bbox)

    assert expected_col_limit == returned_col_limit 
    assert expected_row_limit == returned_row_limit


def test_clean_cell_text():
    import pandas as pd
    from table_processing.table_tools import clean_cell_text
    df_messy = pd.DataFrame([['asdf', '|   asdf', 'asdf'],['asdf', 'asdf', 'asdf        ']])
    df_clean = df_messy.applymap(clean_cell_text)
    df_expected = pd.DataFrame([['asdf', 'asdf', 'asdf'],['asdf', 'asdf', 'asdf']])
    comparison = df_clean.compare(df_expected)
    assert comparison.empty

    
def test_remove_duplicate_limits():
    from table_processing.table_tools import remove_duplicate_limits
    limit_list = [0, 0.1, 0.1, 50, 60, 0, 51, 52, -50]
    threshold = 2
    unique = remove_duplicate_limits(limit_list, threshold)
    expected = [-50, 0, 50, 52, 60]
    expected.sort()
    unique.sort()
    assert expected == unique


def test_within_threshold():
    from table_processing.table_tools import within_threshold
    assert within_threshold(1, 1, 1) == True
    assert within_threshold(1, 5, 1) == False
    assert within_threshold(1.3, 1.4, 1) == True
    assert within_threshold(1.3, 1.4, 0.01) == False
