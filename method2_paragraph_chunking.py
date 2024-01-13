import numpy as np
import pandas as pd
import wikipediaapi

# Call the Wikipedia function through a user_agent and specify the language
# This code creates an instance of the Wikipedia class from the wikipedia-api package, which is used to interact with the Wikipedia API.

string = "SemSearchDemo/2.0 (Jasper B)" # This line creates a string that will be used as the user agent for the Wikipedia API requests. The user agent is a string that the client sends to the server to identify itself. In this case, it identifies the client as "SemSearchDemo/2.0 (Jasper B)".
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en') # This line creates an instance of the Wikipedia class. The user_agent parameter is set to the previously defined string, and the language parameter is set to 'en', which means that the instance will interact with the English version of Wikipedia. The instance is stored in the wiki_wiki variable, which can then be used to make requests to the Wikipedia API.

# Defining some redundant sections
# These redundant sections are not relevant to the movie plot, so we will remove them from the extracted text.
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
# The function extract_wikipedia_page takes a Wikipedia page title as an argument and retrieves the title and text of the corresponding Wikipedia page, if it exists.
def extract_wikipedia_page(page_title):
    page = wiki_wiki.page(page_title) #  This line uses the wiki_wiki object (which should be an instance of wikipediaapi.Wikipedia) to get the Wikipedia page with the title page_title.
    if page.exists(): # This checks if the page exists.
        title = page.title #  If the page exists, this line gets the title of the page.
        paragraphs = [] # This initializes an empty list to store the paragraphs of text from the page.

        # Extract introduction if available
        if page.summary: # This checks if the page has a summary (an introduction section).
            paragraphs.extend(page.summary.split('\n')) #  If the page has a summary, this line splits the summary into paragraphs (assuming that paragraphs are separated by newline characters) and adds them to the paragraphs list.

        # Extract paragraphs from sections
        for section in page.sections: # The for loop iterates over each section in the page.
          if section.title not in redundant_sections: # If the title of the section is not in redundant_sections, 
            extract_paragraphs(section, paragraphs) # it calls the extract_paragraphs function to extract the paragraphs from the section and add them to the paragraphs list.

        return title, paragraphs # returns the title of the page and the list of paragraphs.

    else:
        return None, None # If the page does not exist, the function returns None, None.
    

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
