import json

# json data
json_data_filepath = "data/processed/data.json"

# Open the JSON file in read mode
with open(json_data_filepath, 'r') as json_file:
    # Load JSON data from the file
    data = json.load(json_file)

print(type(data[0]))