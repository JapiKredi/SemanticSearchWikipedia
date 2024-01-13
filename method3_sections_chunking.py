import numpy as np
import pandas as pd
import wikipediaapi
from sentence_transformers import SentenceTransformer, util

# Call the Wikipedia function through a user_agent and specify the language
# This code creates an instance of the Wikipedia class from the wikipedia-api package, which is used to interact with the Wikipedia API.
string = "SemSearchDemo/2.0 (Jasper B)" # This line creates a string that will be used as the user agent for the Wikipedia API requests. The user agent is a string that the client sends to the server to identify itself. In this case, it identifies the client as "SemSearchDemo/2.0 (Jasper B)".
wiki_wiki = wikipediaapi.Wikipedia(user_agent= string, language= 'en') #  creates an instance of the Wikipedia class. The user_agent parameter is set to the previously defined string, and the language parameter is set to 'en', which means that the instance will interact with the English version of Wikipedia. The instance is stored in the wiki_wiki variable, which can then be used to make requests to the Wikipedia API.


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


# Function to extract and store Wikipedia page sections
# The extract_wikipedia_sections function takes a Wikipedia page title as an argument and retrieves the title and sections of the corresponding Wikipedia page, if it exists.
# Each item in the sections list is a tuple containing the title of a section or subsection and its text. The first item is always the introduction, if it exists.
def extract_wikipedia_sections(page_title):
    page = wiki_wiki.page(page_title) # uses the wiki_wiki object (which should be an instance of wikipediaapi.Wikipedia) to get the Wikipedia page with the title page_title.
    if page.exists(): # checks if the page exists.
        title = page.title #  If the page exists, this line gets the title of the page.
        sections = [] # This initializes an empty list to store the sections of the page.

        # Extract introduction if available
        introduction = page.summary # gets the summary (introduction) of the page
        if introduction:
            sections.append(("Introduction", introduction)) # If the introduction exists, this line adds a tuple containing the string "Introduction" and the introduction text to the sections list.

        # Extract all sections and subsections recursively
        # The recursive_extraction function is defined.
        # This function takes a section as an argument, adds the section's title and text to the sections list (if the text exists), and then calls itself recursively for each subsection of the section. 
        # This means that it will extract the title and text of the section and all its subsections.
        def recursive_extraction(section): # 
            section_text = section.text # gets the text of the section
            if section_text: # checks if the section has text
                sections.append((section.title, section_text)) # If the section has text, this line adds a tuple containing the section's title and text to the sections list.
            for sub_section in section.sections: # The for loop iterates over each subsection in the section.
                recursive_extraction(sub_section) # For each subsection, the recursive_extraction function is called recursively.

        for section in page.sections: # The for loop iterates over each section in the page.
            if section.title not in redundant_sections: # If the title of the section is not in redundant_sections,
                recursive_extraction(section) # it calls the recursive_extraction function to extract the section and its subsections.

        return title, sections # returns the title of the page and the list of sections.

    else:
        return None, None # If the page does not exist, the function returns None, None.


# List of Wikipedia page titles
page_titles = ["The Shawshank Redemption", "The Dark Knight", "Pulp Fiction", "The Godfather", "Goodfellas"]

# Initialize lists to store data
titles = []
section_titles = []
section_texts = []

# Extract data and store in lists
for title in page_titles: # a loop that iterates over each title in the page_titles list.
    extracted_title, extracted_sections = extract_wikipedia_sections(title) # For each title, the extract_wikipedia_sections function is called to extract the title and sections of the corresponding Wikipedia page.
    if extracted_title and extracted_sections: # If the title and sections exist,
        for section_title, section_text in extracted_sections: # the for loop iterates over each section in the sections list.
            titles.append(extracted_title) # For each section, the title of the page is added to the titles list.
            section_titles.append(section_title) # For each section, the title of the section is added to the section_titles list.
            section_texts.append(section_text) # For each section, the text of the section is added to the section_texts list.

# Create a DataFrame
data = {'Title': titles, 'Section Title': section_titles, 'Chunk Text': section_texts} # The data dictionary is created.
section_chunk_df = pd.DataFrame(data) # The DataFrame is created from the data dictionary.

# Display the DataFrame
section_chunk_df = section_chunk_df[section_chunk_df['Chunk Text'] != '']  # Remove empty sections
section_chunk_df = section_chunk_df.reset_index(drop=True)  # Reset index
print(section_chunk_df)

# Function to generate embeddings for text
def generate_embeddings(texts):
    embeddings = embedder.encode(texts, convert_to_tensor=True)
    return embeddings

def generate_embeddings_on_df(df):
  df['Embeddings'] = df['Chunk Text'].apply(lambda x: generate_embeddings([x])[0])
  
# Create embeddings for 'Chunk Text' column on all three dataframes
generate_embeddings_on_df(section_chunk_df)

