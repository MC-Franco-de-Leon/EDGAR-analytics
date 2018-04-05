# EDGAR-analytics
Data engineering for Electronic Data Gathering, Analysis and Retrieval (Insight Challenge)
## Description:
In this repository, we present a python code to solve an Insight data engineering challenge 
https://github.com/InsightDataScience/edgar-analytics
# The problem we are solving:
We are given two input files (inside the input folder) log.csv and inactivity_period.txt

## About log.csv
This file contains data obtained from  Electronic Data Gathering, Analysis and Retrieval (EDGAR) system
https://www.sec.gov/dera/data/edgar-log-file-data-set.html
with information of users accessing the system to retrieve financial information. Our task is to write a code to identify when users have started a new session, compute the length (in time) of the session, and the number of documents they access during the visit. 

The first line of the log.csv file is a header. For the purpose of this challenge we are only interested in the following fields

ip: Which uniquely identifies users --

date: date of the request (yyyy:mm:ss)

time: time of the request (hh:mm:ss)

cik: Security and Exchange Commission's (SEC) Central index key

accession: SEC document accession number

extention: Value that helps determine the document requested

The last three fields uniquely identify the requested documents
