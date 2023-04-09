import json

# Data to be saved
data = {
    "name": "John Doe"
}

# File name to save data
filename = "boundermap.json"

# Write data to file
with open(filename, "w") as file:
    json.dump(data, file)
