import json

# Load the JSON data from a file
with open('data/categoryfreq.json', 'r') as file:
    data = json.load(file)

# Remove entries with values less than 10
data = {key: value for key, value in data.items() if value >= 50}

# Save the modified data back to the file
with open('data/categoryfreq.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Entries with values less than 10 have been removed.")