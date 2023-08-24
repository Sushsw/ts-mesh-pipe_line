import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

# URL of the webpage
url = "https://www.datacommons.org/"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page using Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find all article elements on the page
articles = soup.find_all("article")

# Initialize lists to store extracted data
titles = []
descriptions = []
units = []
links = []
urls = []
sources = []
notes = []
additional_comments = []

# Loop through each article and extract the required information
for article in articles:
    # Extract the title of the article
    title = article.find("h3").get_text(strip=True)
    titles.append(title)

    # Initialize variables to store extracted data
    description = ""
    unit = ""
    link = ""
    url = ""
    source = ""
    note = ""
    additional_comment = ""

    # Extract the paragraphs within the article
    paragraphs = article.find_all("p")

    # Loop through each paragraph and extract relevant information
    for paragraph in paragraphs:
        # Extract the content of the paragraph
        paragraph_text = paragraph.get_text(strip=True)

        # Extract link, url, and source information
        if "source:" in paragraph_text.lower():
            source = paragraph.find("a")["href"]
        if "href=" in str(paragraph):
            link = paragraph.find("a")["href"]
            if "http" in link:
                url = link

        # Customize extraction based on the topic or paragraph content
        if "Biogenic emissions" in paragraph_text:
            description = paragraph_text
            unit = "trillion triples"
        elif "time series" in paragraph_text:
            description = paragraph_text
            unit = "billion"
        elif "million places" in paragraph_text:
            description = paragraph_text
            unit = "million"
        elif "variables" in paragraph_text:
            description = paragraph_text
            unit = "thousand"

    # Append extracted data to lists
    descriptions.append(description)
    units.append(unit)
    links.append(link)
    urls.append(url)
    sources.append(source)
    notes.append(note)
    additional_comments.append(additional_comment)

# Create a DataFrame from the extracted data
data = {
    "Primary Fields": titles,
    "Description": descriptions,
    "Units": units,
    "Link": links,
    "URL": urls,
    "Source": sources,
    "Notes": notes,
    "Additional Comments": additional_comments
}
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("OutputData.csv", index=False)

# Scatter plot example
plt.figure(figsize=(10, 6))
plt.scatter(df['Primary Fields'], df['Units'], color='blue')
plt.title('Data Units Scatter Plot')
plt.xlabel('Primary Fields')
plt.ylabel('Units')
plt.xticks(rotation=90)
plt.tight_layout()

# Save the scatter plot as an image
#plt.savefig('scatter_plot.png')

print("CSV file and scatter plot have been created.")

# Show the scatter plot
plt.show()
