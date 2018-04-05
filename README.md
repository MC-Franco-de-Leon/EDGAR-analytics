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

**ip**: Which uniquely identifies users 

**date**: date of the request (yyyy:mm:ss)

**time**: time of the request (hh:mm:ss)

**cik**: Security and Exchange Commission's (SEC) Central index key

**accession**: SEC document accession number

**extention**: Value that helps determine the document requested

The last three fields uniquely identify the requested documents

## About inactivity_period.txt

This file contains (in the first line) a single integer value between one and 86400 to specify the length of time for which a particular session will be consider closed.

## src code and Output file
 
Following the specifications of the challenge, the main code is in the folder src and is called   

sessionization.py  

The Output file can be found inside the folder output with the name   

sessionization.txt  

This is a text file containing the information of user's sessions with the following format

* IP
* date and time of the first webpage requested in the session (yyyy-mm-dd hh:mm:ss)
* date and time of the last webpage requested in the session (yyyy-mm-dd hh:mm:ss)
* duration of the session in seconds
* count of webpage requests during the session

## Restrictions and possible improvements

* This code is considering that a session can be open for days, but not for months. The algorithm to compute the amount of seconds between the first and last query can be improved by considering moths and years too (I don't know how realistic that might be). Precisely, when doing the count of days for a year, that is a quanitity that may change if we are dealing with a leap year or not. So, we are considering years of 365 days (in order to avoid floating points).
