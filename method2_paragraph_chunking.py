import numpy as np
import pandas as pd
import wikipediaapi

# Call the Wikipedia function through a user_agent and specify the language
string = "SemSearchDemo/2.0 (Jasper B)"
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en')

# Defining some redundant sections

redundant_sections = [
    "See also",
    "References",
    "External links",
    "Further reading",
    "Footnotes",
    "Bibliography",
    "Sources",
    "Citations",
    "Literature",
    "Footnotes",
    "Notes and references",
    "Photo gallery",
    "Works cited",
    "Photos",
    "Gallery",
    "Notes",
    "References and sources",
    "References and notes",
]

# Function to extract and store Wikipedia page information

def extract_wikipedia_page(page_title):
    page = wiki_wiki.page(page_title)
    if page.exists():
        title = page.title
        paragraphs = []

        # Extract introduction if available
        if page.summary:
            paragraphs.extend(page.summary.split('\n'))

        # Extract paragraphs from sections
        for section in page.sections:
          if section.title not in redundant_sections:
            extract_paragraphs(section, paragraphs)

        return title, paragraphs

    else:
        return None, None
    
# Function to recursively extract paragraphs from sections
def extract_paragraphs(section, accumulated_text):
    accumulated_text.extend(section.text.split('\n'))
    for sub_section in section.sections:
        extract_paragraphs(sub_section, accumulated_text)

# List of Wikipedia page titles
page_titles = ["The Shawshank Redemption", "The Dark Knight", "Pulp Fiction", "The Godfather", "Goodfellas"]

# Initialize lists to store data
titles = []
paragraphs = []

# Extract data and store in lists
for title in page_titles:
    extracted_title, extracted_paragraphs = extract_wikipedia_page(title)
    if extracted_title and extracted_paragraphs:
        titles.extend([extracted_title] * len(extracted_paragraphs))
        paragraphs.extend(extracted_paragraphs)

# Create a DataFrame
data = {'Title': titles, 'Chunk Text': paragraphs}
para_chunk_df = pd.DataFrame(data)

# Display the DataFrame
para_chunk_df = para_chunk_df[para_chunk_df['Chunk Text'] != '']  # Remove empty paragraphs
para_chunk_df = para_chunk_df.reset_index(drop=True)   # Reset index
print(para_chunk_df)

