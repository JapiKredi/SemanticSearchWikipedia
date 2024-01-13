import numpy as np
import pandas as pd
import wikipediaapi
from sentence_transformers import SentenceTransformer, util

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
# function takes a Wikipedia section and a list of accumulated text as arguments. 
# It extracts the text from the section and its subsections, splits it into paragraphs, and adds the paragraphs to the accumulated text.
def extract_paragraphs(section, accumulated_text):
    accumulated_text.extend(section.text.split('\n')) # splits the text of the section into paragraphs (assuming that paragraphs are separated by newline characters) and adds them to the accumulated_text list.
    for sub_section in section.sections: #  starts a loop that iterates over each subsection of the section.
        extract_paragraphs(sub_section, accumulated_text) #  the function calls itself recursively for each subsection. This means that it will extract the text from the subsection and its subsections, split it into paragraphs, and add the paragraphs to the accumulated_text list.

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

# Load pre-trained Sentence Transformer model
model_name = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model_name)

# Function to generate embeddings for text
def generate_embeddings(texts):
    embeddings = embedder.encode(texts, convert_to_tensor=True)
    return embeddings

def generate_embeddings_on_df(df):
  df['Embeddings'] = df['Chunk Text'].apply(lambda x: generate_embeddings([x])[0])
  
# Create embeddings for 'Chunk Text' column on all three dataframes
generate_embeddings_on_df(para_chunk_df)

# printing the dataframe that includes the embeddings 
print(para_chunk_df)

print(para_chunk_df['Embeddings'][0])