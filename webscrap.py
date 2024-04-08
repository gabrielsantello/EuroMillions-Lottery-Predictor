import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table on the webpage
    table = soup.find_all('table')[0] 

    # Create a list to hold all the data from the table
    data = []

    # Find all the rows in the table and loop through them
    for row in table.find_all('tr'):
        cols = row.find_all('td')

        # Get the text from each column in the row
        cols = [col.text.strip().replace('\u202f', ' ').replace('\u00a0', ' ') for col in cols]

        # Add the columns to the data array
        data.append(cols)

    return data

def write_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def get_last_scraped_year():
    try:
        with open('last_scraped_year.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 2003

def set_last_scraped_year(year):
    with open('last_scraped_year.txt', 'w') as file:
        file.write(str(year))

# Get the current year
current_year = datetime.now().year

# Get the last scraped year
last_scraped_year = get_last_scraped_year()

# Iterate through the years from the last scraped year to the current year
for year in range(last_scraped_year + 1, current_year + 1):
    url = f"https://www.tirage-euromillions.net/euromillions/annees/annee-{year}/"
    data = scrape_table(url)

    # Write the data to a CSV file
    write_to_csv(data, 'table_data.csv')

    # Update the last scraped year
    set_last_scraped_year(year)

print("Data has been written to 'table_data.csv'")