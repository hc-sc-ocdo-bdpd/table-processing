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
    metrics_df = test_tables({t_name: [trueT,readT]})

    assert metrics_df['Overlap'][t_name] == 1.000  # dimensions
    assert metrics_df['String Similarity'][t_name] == 0.888  # overall contents
    assert metrics_df['Completeness'][t_name] == 0.560  # cell content completeness
    assert metrics_df['Purity'][t_name] == 0.440  # cell content purity
    assert metrics_df['Precision'][t_name] == 0.225  # cell neighbours/location
    assert metrics_df['Recall'][t_name] == 0.225  # cell neighbours/location
