import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


# Test the input bulletproofing on process_pdf()
def test_process_pdf():
    from table_processing.Table_processor_main import process_pdf, default_output
    from pathlib import Path
    import os

    # Bad input path
    input_path = "./tests/resources"
    exception_happened = False
    try:
        process_pdf(input_path)
    except:
        exception_happened = True
    assert(exception_happened)

    # Good input path, good output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/out.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path, output_file_path = output_path)[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(output_path))
    assert(os.path.exists(output_path))
    os.remove(output_path)
    assert not os.path.exists(output_path)

    # Good input path, no provided output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = default_output
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path)[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(output_path))
    assert os.path.exists(output_path)
    os.remove(output_path)
    assert not os.path.exists(output_path)

    # Good input path, bad output path
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    expected_output_path = default_output
    output_path = "asdf"
    if os.path.exists(output_path):
        os.remove(output_path)
    returned_path = process_pdf(input_path, output_file_path = output_path)[0]
    returned_path = Path(returned_path)
    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_process_content():
    from table_processing.Table_processor_main import process_content
    from pathlib import Path
    import os
    import fitz
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/out_test_process_content.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)
    doc = fitz.open(input_path)
    content = doc.tobytes() 
    doc.close()
    returned_path = process_content(content, output_file_path = output_path)[0]
    returned_path = Path(returned_path)
    expected_output_path = output_path
    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_base64_input():
    from table_processing.Table_processor_main import process_content
    from pathlib import Path
    import os
    import fitz
    import base64    

    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/test_base64_input.xlsx"
    if os.path.exists(output_path):
        os.remove(output_path)

    input_file = open(input_path,"rb")
    content_binary = input_file.read()
    data = (base64.b64encode(content_binary))
    content = base64.b64decode(data)

    returned_path = process_content(content, output_file_path = output_path)[0]
    returned_path = Path(returned_path)
    expected_output_path = output_path

    assert(returned_path.match(expected_output_path))
    assert os.path.exists(expected_output_path)
    os.remove(expected_output_path)
    assert not os.path.exists(expected_output_path)


def test_intermediate_output():
    from table_processing.Table_processor_main import process_pdf
    from pathlib import Path
    import shutil as st
    import os
    
    input_path = "./tests/resources/DmZUHweaZfPcMjTCAySRtp.pdf"
    output_path = "./tests/resources/out_test_process_content.xlsx"
    intermediate_path = './tests/resources/intermediate_output'
    if os.path.exists(output_path):
        os.remove(output_path)
    
    if os.path.exists(intermediate_path):
        st.rmtree(intermediate_path)

    returned_path, returned_inter_path = process_pdf(input_path, output_file_path = output_path, input_intermediate_output=True)
    returned_path = Path(returned_path)
    expected_output_path = output_path
    
    returned_inter_path = Path(returned_inter_path)
    expected_inter_path = intermediate_path
    
    assert(returned_path.match(expected_output_path))
    assert(returned_inter_path.match(intermediate_path))
    assert os.path.exists(expected_output_path)
    assert os.path.exists(expected_inter_path)
    os.remove(expected_output_path)
    st.rmtree(expected_inter_path)
    assert not os.path.exists(expected_output_path)
    assert not os.path.exists(expected_inter_path)
