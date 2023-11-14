import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


def test_metrics():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'.xlsx')

    # Compare the two tables and calculate the metrics
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 1.000               # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.888     # overall contents
    assert metrics_df['Completeness'][t_name] == 0.560          # cell content completeness
    assert metrics_df['Purity'][t_name] == 0.440                # cell content purity
    assert metrics_df['Precision'][t_name] == 0.225             # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.225                # cell neighbours/location


def test_metrics_dim_one_cell():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'_one_cell.xlsx')

    # Compare the two tables and calculate the metrics
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 0.040               # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.064     # overall contents
    assert metrics_df['Completeness'][t_name] == 0.040          # cell content completeness
    assert metrics_df['Purity'][t_name] == 1.000                # cell content purity
    assert metrics_df['Precision'][t_name] == 1.000             # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.000                # cell neighbours/location


# test if one column is not recognized
def test_metrics_dim_col_missing():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'_col_missing.xlsx')

    # Compare the two tables and calculate the metrics
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 0.800               # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.656     # overall contents
    assert metrics_df['Completeness'][t_name] == 0.800          # cell content completeness
    assert metrics_df['Purity'][t_name] == 1.000                # cell content purity
    assert metrics_df['Precision'][t_name] == 1.000             # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.775                # cell neighbours/location

# test if one row is not recognized
def test_metrics_dim_row_missing():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'_row_missing.xlsx')

    # Compare the two tables and calculate the metrics
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 0.800               # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.833     # overall contents
    assert metrics_df['Completeness'][t_name] == 0.800          # cell content completeness
    assert metrics_df['Purity'][t_name] == 1.000                # cell content purity
    assert metrics_df['Precision'][t_name] == 1.000             # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.775                # cell neighbours/location