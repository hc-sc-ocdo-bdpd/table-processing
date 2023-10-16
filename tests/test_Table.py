import sys, os
import pytest
sys.path.append(os.path.join(sys.path[0],'table_processing'))


def test_data_frame_exists():
    from huggingface_hub import hf_hub_download
    from PIL import Image
    import pandas as pd
    from table_processing.Table import Table

    file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_table.png")
    table_image = Image.open(file_path).convert("RGB")
    width, height = table_image.size
    table_image.resize((int(width*0.5), int(height*0.5)))
    table = Table(image = table_image)
    assert type(table.get_as_dataframe()) == type(pd.DataFrame())


def test_get_cropped_rows():
    from PIL import Image
    from table_processing.Table import get_cropped_rows

    #Creating image
    row_height = 30
    row_width = 234
    im_red = Image.new('RGB', size = (row_width, row_height), color=(255,0,0))
    im_green = Image.new('RGB', size = (row_width, row_height), color=(0,255,128))
    im_blue = Image.new('RGB', size = (row_width, row_height), color=(0,128,255))
    im = Image.new('RGB', size=(im_red.width, im_red.height + im_green.height + im_blue.height))
    im.paste(im_red, (0,0))
    im.paste(im_green, (0,im_red.height))
    im.paste(im_blue, (0,im_red.height + im_green.height))
    
    #Creating Ditionary holding color and size of each row in image
    color_dict = {(255,0,0): (row_width, row_height), (0,255,128): (row_width, row_height), (0,128,255): (row_width, row_height)}
    dict_items_lst = []
    for item in color_dict.items():
        dict_items_lst.append(item)
    
    #Testing part
    row_limits = [30,60,90]
    row_list = get_cropped_rows(im, row_limits)
    expected_len = len(row_limits)
    assert  expected_len == len(row_list)
    counter = 0
    for row in row_list:
        #Test right dimensions
        if counter > 0:
            assert row.size[1] == round(row_limits[counter] - row_limits[counter-1])
        else:
            assert row.size[1] == round(row_limits[counter])
        #Test right color and pixel match
        assert row_list[counter].getcolors()[0][1] == dict_items_lst[counter][0]
        assert row_list[counter].size == dict_items_lst[counter][1] 
        assert len(row_list[counter].getcolors()) == 1
        assert row_list[counter].getcolors()[0][0] == row.size[0]*row.size[1]
        counter+=1
        

def test_get_cropped_columns():
    from PIL import Image
    from table_processing.Table import get_cropped_columns
    
    #Creating image
    column_height = 30
    column_width = 200
    im_red = Image.new('RGB', size = (column_width, column_height), color=(255,145,35))
    im_green = Image.new('RGB', size = (column_width, column_height), color=(125,255,138))
    im_blue = Image.new('RGB', size = (column_width, column_height), color=(120,150,255))
    im = Image.new('RGB', size=(im_red.width + im_green.width + im_blue.width, column_height))
    im.paste(im_red, (0,0))
    im.paste(im_green, (im_red.width,0))
    im.paste(im_blue, (im_red.width + im_green.width, 0))
    
    #Creating Ditionary holding color and size of each column in image
    color_dict = {(255,145,35): (column_width, column_height), (125,255,138): (column_width, column_height), (120,150,255): (column_width, column_height)}
    dict_items_lst = []
    for item in color_dict.items():
        dict_items_lst.append(item)
    
    #Testing part
    column_limits = [200,400,600]
    column_list = get_cropped_columns(im, column_limits)
    expected_len = len(column_limits)
    assert  expected_len == len(column_list)
    counter = 0
    for column in column_list:
        #Test right dimensions
        if counter > 0:
            assert column.size[0] == round(column_limits[counter] - column_limits[counter-1])
        else:
            assert column.size[0] == round(column_limits[counter])
        #Test right color and pixel match
        assert column_list[counter].getcolors()[0][1] == dict_items_lst[counter][0] 
        assert column_list[counter].size == dict_items_lst[counter][1]
        assert len(column_list[counter].getcolors()) == 1
        assert column_list[counter].getcolors()[0][0] == column.size[0]*column.size[1]
        counter+=1
