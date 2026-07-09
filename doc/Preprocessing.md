# Preamble

The preprocessing scripts neccessary to prepare the training data is stored in src/data. The macro \$TOP refers to the 
top directory of the checked out code, and \$DATA the place you store the data

# Steps
1. Create an account at kystdatahuset.no to access utility functions.
2. Prepare the data directories for ERS and AIS. You might copy the structure/data found on gpusrv1:/data/cofud
3. Now, work in the directory $TOP/src/data
4. Initially, generate a token for the API access to kystdatahuset by inserting the username/password in authenticate.py
5. Put the token in radio2mmsi.py right after "Authorization": "Bearer 
6. Run the createmmsi4radio_recursive.py \$DATA/ERS to generate the file radio2mmsi.csv
7. Create a directory $DATA/csv
8. Run this command: ```python3 ais_ers_preprocessing_with_legacy.py $DATA --radio2mmsi ./radio2mmsi.csv --ports-csv ./ports.csv --csv-dir $DATA/csv <YEAR>.``` You will have to run the command for each year of data you have available.

