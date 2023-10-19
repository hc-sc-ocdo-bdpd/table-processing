import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


variable_names = "parameter, value"
values = [('Overlap', 1.000),               # dimensions
          ('String Similarity', 0.888),     # overall contents
          ('Completeness', 0.560),          # cell content completeness
          ('Purity', 0.440),                # cell content purity
          ('Precision', 0.225),             # cell neighbours/location
          ('Recall', 0.225)]                # cell neighbours/location


@pytest.fixture
def metrics_df():
    import pandas as pd
    from table_processing.table_metrics import test_tables

    # Import true and processed tables
    t_name = 'test_metrics'
    file_path = './tests/resources/' + t_name + '/'  + t_name
    trueT = pd.read_excel(file_path+'_true.xlsx')
    readT = pd.read_excel(file_path+'.xlsx')

    # Compare the two tables and calculate the metrics
    metrics_df = test_tables({t_name: [trueT,readT]})
    yield metrics_df, t_name


@pytest.mark.parametrize(variable_names, values)
def test_metrics(parameter, value, metrics_df):
    metrics_df, t_name = metrics_df
    assert metrics_df[parameter][t_name] == value
