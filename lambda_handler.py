#!/usr/bin/env python

import json

# Import any libraries you need

import requests

## Do not edit
class VerkadaDB():
    def __init__(self):
        self._data = {}
	      ## You may add to the class definition below this line
        self.entry_count = {}
        
## To-do: add class methods
    def addTable(self, tableName):
        if tableName in self._data:
            return "Table already exists in the database."
        self._data[tableName] = {}
        self.entry_count[tableName] = 0
        
    def addRow(self, tableName, rowData):
        # Since first name and company is not enough to distinguish.
        # if rowData['email'] in self._data[tableName]['email'].values():
            # return "Row already exists in the table."

        for k, v in rowData.items():
            # If key exists in table
            if k not in self._data[tableName]:
                self._data[tableName][k] = {}
            self._data[tableName][k][self.entry_count[tableName]] = v

        print(self._data)
        self.entry_count[tableName] += 1

    def __getMatchingRowIndices(self, tableName, matchingCriteria):
        indices_of_potential_matches = []

        for criteria_key, critera_value in matchingCriteria.items():
            if criteria_key in self._data[tableName]:
                column_values = self._data[tableName][criteria_key]
                for k, v in column_values.items():
                    if critera_value == v:
                        indices_of_potential_matches.append(k)

        # For a row to match all criteria it needs to appear N times in
        # indices_of_potential_matches where N is len(matchingCriteria)
        unique_indices = list(set(filter(lambda x: indices_of_potential_matches.count(x) == len(matchingCriteria),
                                         indices_of_potential_matches)))
        
        return unique_indices

    def __getMatchingRowIndicesComparators(self, tableName, matchingCriteria):
        indices_of_potential_matches = []

        for criteria_key, critera_value in matchingCriteria.items():
            if criteria_key in self._data[tableName]:
                column_values = self._data[tableName][criteria_key]
                for k, v in column_values.items():
                    if criteria_key == "age":
                        parts = critera_value.split()
                        if len(parts) == 2:
                            if parts[0] == "EQ":
                                if v == int(parts[1]):
                                    indices_of_potential_matches.append(k)
                            elif parts[0] == "GT":
                                if v > int(parts[1]):
                                    indices_of_potential_matches.append(k)
                            elif parts[0] == "LT":
                                if v < int(parts[1]):
                                    indices_of_potential_matches.append(k)
                            else:
                                print("Check comparison operator, only LT, GT and EQ allowed.")
                        elif len(parts) == 4:
                            if parts[0] == "LT" and parts[2] == "GT":
                                if v < int(parts[1]) and v > int(parts[3]):
                                    indices_of_potential_matches.append(k)
                            elif parts[0] == "GT" and parts[2] == "LT":
                                if v > int(parts[1]) and v < int(parts[3]):
                                    indices_of_potential_matches.append(k)
                            else:
                                print("Check comparison operator, only LT and GT allowed.")
                        else:
                            print("Comparison criteria must be in the form 'LT/GT/EQ 30' or 'GT/LT 20 LT/GT 40'.")
                    else:
                        if critera_value == v:
                            indices_of_potential_matches.append(k)

        # For a row to match all criteria it needs to appear N times in
        # indices_of_potential_matches where N is len(matchingCriteria)
        unique_indices = list(set(filter(lambda x: indices_of_potential_matches.count(x) == len(matchingCriteria),
                                         indices_of_potential_matches)))
        
        return unique_indices

    # r3 = dbInstance.getRows("leads", {"age": "GT 30 LT 60"})
    def getRows(self, tableName, matchingCriteria):
        unique_indices = self.__getMatchingRowIndicesComparators(tableName, matchingCriteria)

        rows = []
        # Find resulting rows and add them to result
        for idx in unique_indices:
            row = {}
            for k, v in self._data[tableName].items():
                for k1, v1 in v.items():
                    if k1 == idx:
                        row[k] = v1
            rows.append(row)

        return rows
    
    # dbInstance.updateRows("leads", {"name": "Kyle"}, {"age": "26", "nationality": "BA"})
    def updateRows(self, tableName, matchingCriteria, updateInformation):
        # Find row indices that match criteria
        unique_indices = self.__getMatchingRowIndices(tableName, matchingCriteria)

        for idx in unique_indices:
            for k, v in updateInformation.items():
                if k in self._data[tableName]:
                    column_values = self._data[tableName][k]
                    if idx in column_values:
                        # Update row entry
                        self._data[tableName][k][idx] = v
    
    # dbInstance.deleteRows("leads", {"name": "Craig"})
    def deleteRows(self, tableName, matchingCriteria):
        # Find row indices that match criteria
        unique_indices = self.__getMatchingRowIndices(tableName, matchingCriteria)
        
        for idx in unique_indices:
            for k, v in self._data[tableName].items():
                if idx in v:
                    # Delete row entry
                    del self._data[tableName][k][idx]


## Do not edit   
dbInstance = VerkadaDB()

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

    genderize_url = "https://api.genderize.io?name=" + first_name
    genderize_response = requests.get(genderize_url)
    genderize_json = genderize_response.json()
    gender = genderize_json["gender"]

    nationalize_url = "https://api.nationalize.io?name=" + first_name
    nationalize_response = requests.get(nationalize_url)
    nationalize_json = nationalize_response.json()
    countries = nationalize_json["country"]
    nationality = max(countries, key=lambda x: x['probability'])['country_id'] if countries else None

    results = {
        "name": first_name,
        "email": email,
        "domain": domain,
        "topLevelName": top_level_name,
        "age": age,
        "gender": gender,
        "nationality": nationality,
    }

    print(results)

    if domain != "verkada":
        dbInstance.addRow("leads", results)

    headers =  {"Content-Type":"application/json"}
    json_output = json.dumps(results)
    api_url = "https://rwph529xx9.execute-api.us-west-1.amazonaws.com/prod/pushToSlack"
    # push_response = requests.post(api_url, data=json_output, headers=headers)
    # print(push_response.json())
    # print(push_response.status_code)

    ## Output: JSON String which mimics AWS Lambda Output
    return json_output

## To Do: Create a table to hold the information you process
dbInstance.addTable("leads")

## Do not edit
lambda_handler(json.dumps({"email":"John@acompany.com"}))
lambda_handler(json.dumps({"email":"Willy@bcompany.org"}))
lambda_handler(json.dumps({"email":"Kyle@ccompany.com"}))
# lambda_handler(json.dumps({"email":"Georgie@dcompany.net"}))
# lambda_handler(json.dumps({"email":"Karen@eschool.edu"}))
# lambda_handler(json.dumps({"email":"Annie@usa.gov"}))
# lambda_handler(json.dumps({"email":"Elvira@fcompay.org"}))
# lambda_handler(json.dumps({"email":"Juan@gschool.edu"}))
# lambda_handler(json.dumps({"email":"Julie@hcompany.com"}))
# lambda_handler(json.dumps({"email":"Pierre@ischool.edu"}))
# lambda_handler(json.dumps({"email":"Ellen@canada.gov"}))
# lambda_handler(json.dumps({"email":"Craig@jcompany.org"}))
# lambda_handler(json.dumps({"email":"Juan@kcompany.net"}))
# lambda_handler(json.dumps({"email":"Jack@verkada.com"}))
# lambda_handler(json.dumps({"email":"Jason@verkada.com"}))
# lambda_handler(json.dumps({"email":"Billy@verkada.com"}))
# lambda_handler(json.dumps({"email":"Brent@verkada.com"}))

## Put code for Part 2 here

# Update rows for Kyles
dbInstance.updateRows("leads", {"name": "Kyle"}, {"age": 26, "nationality": "BA"})

# Delete rows for Craigs
dbInstance.deleteRows("leads", {"name": "Craig"})

# Get rows
rows = dbInstance.getRows("leads", {"gender": "female", "topLevelName": "gov"})
print(rows)
print("HERE")
# Get rows with comparison operators
r1 = dbInstance.getRows("leads", {"age": "GT 30"})
print(r1)
r2 = dbInstance.getRows("leads", {"age": "LT 60"})
print(r2)
r3 = dbInstance.getRows("leads", {"age": "GT 30 LT 70"})
print(r3)
