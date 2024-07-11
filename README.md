# Tenders Electronic Daily Open Data
![PyPI - Python Version](https://img.shields.io/badge/python-3.12-3776AB?logo=python)    

This project takes the Open Data (OD) from the Tenders Electronic Daily (TED) portal and turns it into an event log.  
TED web page with OD (in English): [https://data.europa.eu/data/datasets/ted-csv?locale=en](https://data.europa.eu/data/datasets/ted-csv?locale=en)  
There are two types of dataset available:  
- CFC: Call For Competition (step 1/2); key feature ID_NOTICE_CN.  
- CAN: Contract Award Notices (step 2/2); key feature ID_NOTICE_CAN.    
- The two datasets are linked by CFC.FUTURE_CAN_ID = CAN.ID_NOTICE_CAN. Note: the CAN of a CFC may be missing, due to the tender (CFC.ID_NOTICE_CN) not having been awarded. ID_NOTICE_CN will represent the case-id in the event log.  

## TED Open Data - Download
Sample URL for CFC: [https://data.europa.eu/api/hub/store/data/ted-contract-notices-2020.zip](https://data.europa.eu/api/hub/store/data/ted-contract-notices-2020.zip)  
Sample URL for CAN: [https://data.europa.eu/api/hub/store/data/ted-contract-award-notices-2020.zip](https://data.europa.eu/api/hub/store/data/ted-contract-award-notices-2020.zip)  
Change the year in the URL to download the related file and save it in ```OD_DIR``` directory inserting 'CFC' or 'CAN' suffix in the file name.  
The 2016 - 2022 files are also available in a public Drive here: [https://bit.ly/3UP53pC](https://bit.ly/3UP53pC). Download CSVs in the ```OD_DIR```  directory.  
At least one CFC and one CAN file must be used to generate the event log correctly.  

## TED Open Data - Documentation
TED CSV open data NOTES & CODEBOOK (PDF): [https://data.europa.eu/api/hub/store/data/ted-csv-data-information-v3-6.pdf](https://data.europa.eu/api/hub/store/data/ted-csv-data-information-v3-6.pdf)  
TED CSV open data Advanced notes on methodology (PDF): [http://data.europa.eu/euodp/en/data/storage/f/2022-02-14T122830/TED_advanced_notes_vers_0.92.pdf](http://data.europa.eu/euodp/en/data/storage/f/2022-02-14T122830/TED_advanced_notes_vers_0.92.pdf)

## > Script Execution
```01_read_opendata.ipynb```  
Reads the 'CFC' and 'CAN' raw OD in ```OD_DIR``` directory, filters them by the countries and contract authority code (defined in the ```config.yml```) and merges them into a single CSV file in the directory defined in ```DATA_DIR```. Create the file defined in ```TED_URLS_FILE``` with a list of URLs from which to download the texts of each CFC. Before executing this script, configure the filters in the JSON defined in ```TED_CONFIG_FILE```.   
```02_stats_opendata.ipynb```  
Create file statistics by country and year after filtering raw TED dataset.   
```03_log_creation.ipynb```  
Join 'CFC' and 'CAN' files and transforms data into an event log. Save the event log generated in ```DATA_DIR```.  The ```ID_NOTICE_CN``` will represent the ```Case ID``` of the event log. It also creates the list of URLs to files containing the full texts of the tenders.  
```04_download_guue.ipynb```  
Starting from the file defined in ```TED_URLS_FILE```, it downloads the linked PDFs in the 'PDF_NOTICE_URL' column of the CSV and saves them in ```GUUE_DIR```. Set the desired language codes for downloading in ```TED_LANG_DOWNLOAD```.    

## > Script Dependencies
See ```requirements.txt``` for the required libraries (```pip install -r requirements.txt```).  

## > Directories
```config```  
Directory with the configuration file in YAML format (```config.yml```) and script to read it (```config_reader.py```).   
```data```  
Contains filtered data and schema from raw OD. Files are saved by entering 'CFC' or 'CAN' to distinguish their type.  
```data_log```  
Contains the event log created starting from the files in ```data```.   
```guue```  
Directory of TED texts in PDF format, downloaded by following the URLs in the file ```TED_URLS_FILE```.  
```opendata```    
Contains raw OD downloaded from the TED web site.   
```stats```    
Contains the results obtained by the script on statistics.  

## Other projects
This project is also related to: [https://github.com/roberto-nai/TED-OD-LLM](https://github.com/roberto-nai/TED-OD-LLM)  

## Share
If you use it, please cite:    
```
@InProceedings{10.1007/978-3-031-47112-4_17,
author="Nai, Roberto
and Sulis, Emilio
and Genga, Laura",
editor="Sales, Tiago Prince
and Ara{\'u}jo, Jo{\~a}o
and Borbinha, Jos{\'e}
and Guizzardi, Giancarlo",
title="Automated Analysis with Event Log Enrichment of the European Public Procurement Processes",
booktitle="Advances in Conceptual Modeling",
year="2023",
publisher="Springer Nature Switzerland",
address="Cham",
pages="178--188",
isbn="978-3-031-47112-4"
}
```