#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import os

url = "https://wiki.kiwix.org/wiki/Content_in_all_languages"
response = requests.get(url, stream=True)
response.raise_for_status()  # Raise an error for bad responses
total_size = int(response.headers.get('content-length', 0))
block_size = 1024

# Read the HTML content into memory
html_content = b""
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading HTML")
for data in response.iter_content(chunk_size=block_size):
    html_content += data
    progress_bar.update(len(data))
progress_bar.close()

# Convert the binary content to a string
html_content = html_content.decode('utf-8')

# Create a CSV file to write the data
csv_filename = 'data/zim_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row
    header = ['Project', 'Language', 'Size', 'Date created', 'Number of articles / Flavour', 'Direct URL', 'SHA256 URL', 'Torrent URL', 'Magnet URL']
    writer.writerow(header)

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get the data rows
    rows = soup.find('table', {'id': 'zimtable'}).find_all('tr')[1:]

    # Write the data rows with tqdm for progress bar
    for row in tqdm(rows, desc="Scraping data"):
        # Extract text content from all <td> elements
        data = [td.text.strip() for td in row.find_all('td')[:-1]]  # Exclude the last <td>

        # Extract URLs from the last <td> (nested anchor tags)
        urls = row.find_all('td')[-1].find_all('a')

        # Extract individual URLs and add them to the data list
        for url in urls:
            data.append(url['href'])

        # Add the row to the CSV file
        writer.writerow(data)

# Replace Windows line endings with Unix line endings in the CSV file
with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
    csv_content = csv_file.read()
csv_content = csv_content.replace('\r\n', '\n')
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_file.write(csv_content)

os.system(f"7z a -mx=9 {csv_filename}.7z {csv_filename}")

print(f"Data has been scraped and saved to {csv_filename}.")

