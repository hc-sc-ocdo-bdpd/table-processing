# Table Processing Library

This library contains tools for extracting data from scanned tables in PDF files. This is experimental software that is under development.

## Dependencies

This project has dependencies defined in `requirements.txt`. These dependencies should be installed using `pip3 install -r depencencies.txt`. Older versions of pip may result in an error.

Additionally, this project uses tesseract for OCR. This must be installed at: `C:/Users/USERNAME/AppData/Local/Programs/Tesseract-OCR/tesseract.exe`. See https://github.com/UB-Mannheim/tesseract/wiki.

The table detection performance tests use MikTex (https://miktex.org/download) for generating artificial test case tables. This needs to be installed at it's default location (C:\Users\USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe).

## Running the Table Extraction Tool

There are two versions of the table extraction tool: a command line version and a graphical version which runs in a web browswer.

- Command line version implementation: table_processing/Table_processor_main.py
- GUI version: table_processing/GUI.py. Once running, point your browser to http://127.0.0.1:8050/ to see it.

## Structure

This library contains several components in different directories:

- table_processing: Table extraction tools
- tests: pytest test cases
- table_trials_results: Results in .xlsx format of the tests run on generated tables with a variety of randomized parameters including rows, columns, vertical/horizontal lines, font size, row height, margin, orientation, and special characters. Parameter values and performance metrics are tracked for each of the roughly 7000 generated tables along with overall summaries for each individual metric (mean, stdev, min, max, median, etc.).

These include file processing tools (in the file_processing directory). This code is structured as follows:

- `table_processing.Table_Detector`: Entry point for the table processing tools.
- `table_processing.benchmark_pipeline`: Performance testing pipeline for the table_processing components.

## Randomized Generated Table Tests

- Running these table generation tests starts in the benchmark_pipeline.py script which calls the GeneratedTable, Table_Detector, & Table classes.
  - When this script calls the GeneratedTable class, its parameters can be customized to fit whatever test is needed to run.
- Once all the results have been exported, named appropriately, and placed in the table_trials_results directory, the metrics_results.py script can be run which combines all the results into the table_metrics_ALL.xlsx file.
  - This sheet holds data for each individual table, a summary of all the metrics, the results grouped by each different combination of the parameters, and the results grouped by every individual value of every parameter.
  - This facilitates the analysis to discern on which parameters (and specific combination of parameters) the table extraction model performs well and poorly.
- Results after 2 randomized runs spanning nearly 12K generated tables:
  - OCR struggles with special characters & diacritics
  - Marginally better performance with visible horizontal lines and without vertical lines
  - Poor performance on low-dimensional tables (1-2 rows/columns)
  - Top of page margin has seemingly no effect
  - No significant difference when changing page orientation, with a slight edge to portrait over landscape
  - Somewhat similar and acceptable model performance with row height in the range of 1.25 to 2.50
  - Performance diminishes as font size nears 20 and drops off significantly as it enters the early 20s (almost inept once it hits 24)
- Future work:
  - Testing has yet to be conducted on multi-rows/merged cells
  - Re-evaluate row & column pixel thresholds
  - Identified row limits gradually shift out of alignment before self-correction around the 30 row mark
- More in-depth information on the testing results & future work is available in issue #65

## Build executable
Run the `table_processing/build.py` script. The intermediate output will be in the `build` directory. The final executable will be in the `dist` directory.
