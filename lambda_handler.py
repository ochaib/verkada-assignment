#!/usr/bin/env python

import json

# Import any libraries you need

## Do not edit
class VerkadaDB():
    def __init__(self):
        self._data = {}
	      ## You may add to the class definition below this line
        
## To-do: add class methods
    def addTable(self, tableName):
        pass
        
    def addRow(self,tableName, rowData):
        pass
    
    def getRows(self,tableName, matchingCriteria):
        pass
    
    def updateRows(self, tableName, matchingCriteria, updateInformation):
        pass
    
    def deleteRows(self,tableName, matchingCriteria):
        pass

## Do not edit   
dbInstance = VerkadaDB()  

## To-do: Implement Function (mimics AWS Lambda handler)
## Input: JSON String which mimics AWS Lambda input
def lambda_handler(json_input):
    global dbInstance

    json_output = json.dumps({})
    ## Output: JSON String which mimics AWS Lambda Output
    return json_output

## To Do: Create a table to hold the information you process
    

## Do not edit
lambda_handler(json.dumps({"email":"John@acompany.com"}))
lambda_handler(json.dumps({"email":"Willy@bcompany.org"}))
lambda_handler(json.dumps({"email":"Kyle@ccompany.com"}))
lambda_handler(json.dumps({"email":"Georgie@dcompany.net"}))
lambda_handler(json.dumps({"email":"Karen@eschool.edu"}))
lambda_handler(json.dumps({"email":"Annie@usa.gov"}))
lambda_handler(json.dumps({"email":"Elvira@fcompay.org"}))
lambda_handler(json.dumps({"email":"Juan@gschool.edu"}))
lambda_handler(json.dumps({"email":"Julie@hcompany.com"}))
lambda_handler(json.dumps({"email":"Pierre@ischool.edu"}))
lambda_handler(json.dumps({"email":"Ellen@canada.gov"}))
lambda_handler(json.dumps({"email":"Craig@jcompany.org"}))
lambda_handler(json.dumps({"email":"Juan@kcompany.net"}))
lambda_handler(json.dumps({"email":"Jack@verkada.com"}))
lambda_handler(json.dumps({"email":"Jason@verkada.com"}))
lambda_handler(json.dumps({"email":"Billy@verkada.com"}))
lambda_handler(json.dumps({"email":"Brent@verkada.com"}))

## Put code for Part 2 here