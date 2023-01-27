#!/usr/bin/env python

import json

# Import any libraries you need

import requests

## Do not edit
class VerkadaDB():
    def __init__(self):
        self._data = {}
	      ## You may add to the class definition below this line
        
## To-do: add class methods
    def addTable(self, tableName):
        if tableName in self._data:
            return "Table already exists."
        else:
            self._data[tableName] = {}
        
    def addRow(self, tableName, rowData):
        # What is row data? Example of what it looks like?
        if rowData in self._data[tableName]:
            return "Row already exists."
        else:
            self._data[tableName] = rowData
    
    def getRows(self, tableName, matchingCriteria):
        # What is matching criteria?
        self._data[tableName]
    
    def updateRows(self, tableName, matchingCriteria, updateInformation):
        pass
    
    def deleteRows(self,tableName, matchingCriteria):
        pass

## Do not edit   
dbInstance = VerkadaDB()

dbInstance.addTable("Leads")

## To-do: Implement Function (mimics AWS Lambda handler)
## Input: JSON String which mimics AWS Lambda input
def lambda_handler(json_input):
    global dbInstance

    # Get first name from json_input
    data = json.loads(json_input)
    email = data["email"]
    first_name = email.split('@')[0]
    domain = email.split('@')[1].split('.')[0]
    top_level_name = email.split('@')[1].split('.')[1]
    print(email)

    # Fetch result from URLs
    agify_url = "https://api.agify.io?name=" + first_name
    agify_response = requests.get(agify_url)
    agify_json = agify_response.json()
    age = agify_json["age"]
    print(agify_json)

    genderize_url = "https://api.genderize.io?name=" + first_name
    genderize_response = requests.get(genderize_url)
    genderize_json = genderize_response.json()
    gender = genderize_json["gender"]
    print(genderize_json)

    nationalize_url = "https://api.nationalize.io?name=" + first_name
    nationalize_response = requests.get(nationalize_url)
    nationalize_json = nationalize_response.json()
    countries = nationalize_json["country"]
    nationality = max(countries, key=lambda x: x['probability'])['country_id'] if countries else None
    print(nationalize_json)
    print(nationality)

    results = {
        "name": first_name,
        "email": email,
        "domain": domain,
        "topLevelName": top_level_name,
        "age": age,
        "gender": gender,
        "nationality": nationality,
    }

    dbInstance.addRow("Leads", results)

    print(results)

    json_output = json.dumps(results)
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