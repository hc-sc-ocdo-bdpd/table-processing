import sys, os
import pytest
from pathlib import Path
sys.path.append(os.path.join(sys.path[0],'table_processing'))


@pytest.fixture()
def bad_input_path():
    yield "./tests/resources"


@pytest.fixture()
def good_input_path():
    yield "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    

@pytest.fixture(scope = "session")
def good_output_path(tmp_path_factory):
    yield str(tmp_path_factory.mktemp("data") / "out.xlsx")


@pytest.fixture(scope = "session")
def intermediate_path(good_output_path):
    output_dir = Path(good_output_path).parents[0]
    yield str(output_dir) + '/intermediate_output/'


@pytest.fixture(scope = "function")
def default_output():
    from table_processing.Table_processor_main import default_output
    if os.path.exists(default_output):
        os.remove(default_output)
    yield default_output
    if os.path.exists(default_output):
        os.remove(default_output)


# Test the input bulletproofing on process_pdf()
# Bad input path
def test_process_pdf_bad_input_path(bad_input_path):
    from table_processing.Table_processor_main import process_pdf
    exception_happened = False
    try:
        process_pdf(bad_input_path)
    except:
        exception_happened = True
    assert(exception_happened)


# Test the input bulletproofing on process_pdf()
# Good input path, good output path
def test_process_pdf_good_input_path_good_output_path(good_input_path, good_output_path):
    from table_processing.Table_processor_main import process_pdf
    returned_path = process_pdf(good_input_path, output_file_path = good_output_path)[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(good_output_path))
    assert(os.path.exists(good_output_path))


# Test the input bulletproofing on process_pdf()
# Good input path, no provided output path
def test_process_pdf_good_input_path_no_output_path(good_input_path, default_output):
    from table_processing.Table_processor_main import process_pdf
    returned_path = process_pdf(good_input_path)[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(default_output))
    assert os.path.exists(default_output)


# Test the input bulletproofing on process_pdf()
# Good input path, bad output path
def test_process_pdf_good_input_path_bad_output_path(good_input_path, default_output):
    from table_processing.Table_processor_main import process_pdf
    returned_path = process_pdf(good_input_path, output_file_path = "asdf")[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(default_output))
    assert os.path.exists(default_output)


def test_process_content(good_input_path, good_output_path):
    from table_processing.Table_processor_main import process_content
    import fitz

    doc = fitz.open(good_input_path)
    content = doc.tobytes() 
    doc.close()
    returned_path = process_content(content, output_file_path = good_output_path)[0]
    returned_path = Path(returned_path)
    expected_output_path = good_output_path
    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)


def test_base64_input(good_input_path, good_output_path):
    from table_processing.Table_processor_main import process_content
    import base64    

    input_file = open(good_input_path,"rb")
    content_binary = input_file.read()
    data = (base64.b64encode(content_binary))
    content = base64.b64decode(data)
    returned_path = process_content(content, output_file_path = good_output_path)[0]
    returned_path = Path(returned_path)
    expected_output_path = good_output_path

    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)


def test_intermediate_output(good_input_path, good_output_path, intermediate_path):
    from table_processing.Table_processor_main import process_pdf
    returned_path, returned_inter_path = process_pdf(good_input_path, output_file_path = good_output_path, input_intermediate_output=True)
    returned_path = Path(returned_path)
    returned_inter_path = Path(returned_inter_path)
    assert(returned_path.match(good_output_path))
    assert(returned_inter_path.match(intermediate_path))
    assert os.path.exists(good_output_path)
    assert os.path.exists(intermediate_path)
