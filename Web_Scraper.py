import json
import requests
from bs4 import BeautifulSoup
import sys

# read the JSON file and load its contents
with open(sys.argv[1], 'r') as f:
    json_data = json.load(f)

# extract the URLs from the JSON data
URLs = [data["url"] for data in json_data]

# scrape the web pages and add the text and date to the JSON data
import re

# scrape the web pages and add the text and date to the JSON data
for i, url in enumerate(URLs):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text().replace('\n', '')

    # Locate the date element correctly
    date_elements = soup.find_all('dd', class_='gem-c-metadata__definition')
    date = None
    if len(date_elements) >= 2:
        date_element = date_elements[1]  # Get the second instance
        date = date_element.text.strip()

    json_data[i]["content"] = text
    json_data[i]["date"] = date if date else "Date not found"






# write the updated JSON data to a new file
with open('updated_' + sys.argv[1], 'w') as f:
    json.dump(json_data, f, indent=2)

print(f'{len(URLs)} pages scraped and added to the new JSON file.')
