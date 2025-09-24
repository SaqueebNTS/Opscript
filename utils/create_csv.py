import csv

def create_csv(file_name, data):
    """Creates a CSV file from the provided data."""
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

