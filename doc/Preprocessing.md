# Preamble

The preprocessing scripts neccessary to prepare the training data is stored in src/data. The macro ```$TOP``` refers to the 
top directory of the checked out code, and ```$DATA``` the place you store the data

## Steps if you need to regenerate mapping from radiocallsigns to MMSI for the vessels in the data
1. Create an account at kystdatahuset.no to access utility functions.
2. Prepare the data directories for ERS and AIS. You might copy the structure/data found on ```gpusrv1.cs.uit.no:/data/cofud```
3. Now, work in the directory ```$TOP/src/data```
4. Initially, generate a token for the API access to kystdatahuset by inserting the username/password in ```API_authenticate.py```
5. Put the token in ```API_radio2mmsi.py``` right after "Authorization": "Bearer
6. Run the ```radiocallsign2mmsi.py $DATA/ERS``` to generate the file ```radio2mmsi.csv```

## Steps for preprocessing
1. Create a directory ```$DATA/csv```
2. Create the merged ERS file merge.csv per year using the script ```preprocess_ers_Lovland.py``` and put the produced file in the ```$DATA/AIS/<year>``` catalogue for that year
3. Run this command: ```python ais_ers_preprocessing.py $DATA --radio2mmsi ./radio2mmsi.csv --ports-csv ./ports.csv --csv-dir $DATA/csv <YEAR>.``` You will have to run the command for each year of data you have available.

