import csv
import re
from functools import reduce

def human_readable_to_bytes(size_str):
    # Convert human-readable size to bytes
    size_str = size_str.lower()
    units = {'kb': 1024, 'mb': 1024**2, 'gb': 1024**3, 'tb': 1024**4}
    for unit, multiplier in units.items():
        if unit in size_str:
            return int(re.sub(r'[^\d]', '', size_str)) * multiplier
    return int(size_str)

def bytes_to_human_readable(size_bytes):
    # Convert bytes to human-readable size
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def get_total_size(csv_filename):
    # Read the CSV file and calculate the total size
    total_size = 0
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Skip the header row
        size_index = header.index('Size')

        for row in reader:
            human_readable_size = row[size_index]
            size_in_bytes = human_readable_to_bytes(human_readable_size)
            total_size += size_in_bytes

    return total_size

# Example usage
csv_filename = 'data/zim_data.csv'
total_size_bytes = get_total_size(csv_filename)
total_size_readable = bytes_to_human_readable(total_size_bytes)

print(f'Total Size: {total_size_readable}')

import pandas as pd
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_filename)

# Convert 'Size' column to bytes
df['Size_bytes'] = df['Size'].apply(human_readable_to_bytes)

profile = ProfileReport(df, title="Profiling Report")
profile.to_file("out/your_report.html")

# Group by 'Language' and sum the sizes
grouped_df = df.groupby('Language')['Size_bytes'].sum().reset_index()

# Sort by total size in descending order
grouped_df = grouped_df.sort_values(by='Size_bytes', ascending=False)

# Plot the top N languages by total size
top_n = 10
plt.figure(figsize=(12, 6))
plt.bar(grouped_df['Language'][:top_n], grouped_df['Size_bytes'][:top_n], color='skyblue')
plt.xlabel('Language')
plt.ylabel('Total Size (bytes)')
plt.title(f'Top {top_n} Languages by Total Size')
plt.xticks(rotation=45)
plt.savefig('out/output_plot.png')


