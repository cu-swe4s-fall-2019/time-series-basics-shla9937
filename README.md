# time-series-basics
Time Series basics - importing, cleaning, printing to csv
Note date files are synthetic data. 

inputs you need:
--folder_name: specific folder of .csv files

additional features (to be added):
--output_file: where to save output
--sort_key: str you would like to sort your data on
--number_of_files: number of files to be sorted

You can use the data_import.py file to import datatime and value information from a folder of .csv files. It will round these values nicely and store them as a zip object. Later, we could go in and make this module full functional and allow it to print out specific information that you have input into it.